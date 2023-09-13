from pathlib import Path

from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from letters.models import Letter

from wishtree.settings.prod_settings import EMAIL_HOST_USER

from openpyxl import Workbook
import requests
from bs4 import BeautifulSoup as bs

import re


SPECIAL_SOURCES = ['ozon', 'aliexpress', 'ситилинк', 'wildberries']
SPECIAL_SOURCES_PARAMS = {
    'ozon': 'ozon-bg',
    'wildberries': 'wildberries-bg',
    'aliexpress': 'aliexpress-bg',
    'ситилинк': 'citylink-bg'
}
PRODUCTS_IN_REQUEST = 10
GET_CURRENCY = {
    '$': 'USD',
    '₽': 'RUB',
    '€': 'EUR'
}


class DbToExcel:
    ''' Converter data from 'Letter' model to excel table by 'openpyxl' '''
    row = 2
    USER_EMPTY_DICT = {'email': '', 'phone': '', 'full_name': ''}

    def __init__(self):
        self.book = Workbook()
        self.sheet = self.book.active

        self.sheet['A1'] = 'Имя ребёнка, возраст'
        self.sheet['B1'] = 'Подарок'
        self.sheet['C1'] = 'Фамилия, Имя пользователя'
        self.sheet['D1'] = 'Почта'
        self.sheet['E1'] = 'Телефон'

    def parse_db_data(self) -> list[dict]:
        parsed_list = []
        letters = Letter.objects.all().prefetch_related('gift').prefetch_related('child')
        for letter in letters:
            additional_data = letter.get_user_to_excel() if letter.picked_by else self.USER_EMPTY_DICT
            parsed_list.append(
                {'gift': letter.gift.name, 'child': letter.child.get_full_name(), **additional_data}
            )

        return parsed_list

    def write_to_excel(self, file_name: Path) -> None:
        for letter in self.parse_db_data():
            self.sheet[self.row][0].value = letter['child']
            self.sheet[self.row][1].value = letter['gift']
            self.sheet[self.row][2].value = letter['full_name']
            self.sheet[self.row][3].value = letter['email']
            self.sheet[self.row][4].value = letter['phone']

            self.row += 1

        self.book.save(file_name)
        self.book.close()


class ConfirmEmailMixin:

    def send_confirm_email(self, user):
        current_site = get_current_site(self.request)
        context = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token_generator.make_token(user)
        }
        message = render_to_string('info/send_email_text.html', context=context)
        email_message = EmailMessage(
            'Подтвердите свой email',
            message,
            EMAIL_HOST_USER,
            to=[user.email]
        )

        email_message.send()


def get_rubble_course(currency):
    if currency == 'USD' or currency == 'EUR':
        return 104.72


class SubTextParser:

    def get_converted_text(self, text: str) -> str:
        price = re.findall(r'(?:\d|,|\s)+(?:₽|€|[$])', text)[0]
        # get float number from price with currency symbol
        clean_price = re.findall(r'(?:\d|,|\s)+', price)[0].replace(',', '.').replace(' ', '')

        if not hasattr(self, 'price_currency'):
            currency = GET_CURRENCY[re.findall(r'₽|€|[$]', price)[-1]]
            self.price_currency = get_rubble_course(currency) if not currency == 'RUB' else 1

        new_price = f"{'%.2f' % (float(clean_price) * self.price_currency)} ₽"

        return text.replace(price, new_price)


class ParseShops:

    def __init__(self, soup: bs):
        self.parsed_shops = []
        cards = soup.find_all('div', class_='X7NTVe')

        for card in cards:
            try:
                name, address = card.find('a').find('div').find('div').contents[:2]
            except ValueError:
                continue

            drop_element = address.find('div').find('span')
            if drop_element:
                drop_element.clear()

            parsed_address = re.findall(r'.+(?:Закрыто|Открыто)', address.text)
            address = (
                parsed_address[0].replace('Открыто', '').replace('Закрыто', '') if parsed_address else address.text
            )

            self.parsed_shops.append({'name': name.get_text(), 'address': address})


class ParseGoods:
    SYMBOLS_IN_STRING = 25

    def __init__(self, soup: bs):
        self.parsed_goods = []
        cards = soup.find_all('div', class_='u30d4')
        text_parser = SubTextParser()

        for card_container in cards:
            if not (card := card_container.select_one(':nth-child(2)')):
                continue

            try:
                name, shop = card.contents[:2]
                # google has special symbols before link on product itself we need only link
                product_link = name.find('a').get('href')
                sub_text = shop.get_text()
                name = name.get_text()
                sub_text = text_parser.get_converted_text(sub_text.replace(u'\xa0', u' '))
                image_url = card_container.find('img').get('src')
            except Exception as e:
                continue

            # here check that is sub_text has text from SPECIAL_SOURCES list if has we get class for css styles
            special_param = [SPECIAL_SOURCES_PARAMS[source] for source in SPECIAL_SOURCES if source in sub_text.lower()]
            bg_class = special_param[0] if special_param else ''
            # get first 20 symbols if string is too long and add three dots
            name = f'{name[:self.SYMBOLS_IN_STRING]}...' if len(name) > self.SYMBOLS_IN_STRING else name
            sub_text = f'{sub_text[:self.SYMBOLS_IN_STRING]}...' if len(sub_text) > self.SYMBOLS_IN_STRING else sub_text

            self.parsed_goods.append(
                {
                    'img': image_url, 'name': name,
                    'sub_text': sub_text, 'link': self.convert_to_link(product_link),
                    'bg_class': bg_class
                }
            )

        self._filter_parsed_goods()

    def _filter_parsed_goods(self):
        special_products = list(filter(lambda product: product['bg_class'], self.parsed_goods))
        if len(special_products) >= PRODUCTS_IN_REQUEST:
            self.parsed_goods = special_products[:PRODUCTS_IN_REQUEST]
        else:
            self.parsed_goods = self.parsed_goods[:PRODUCTS_IN_REQUEST]

    @staticmethod
    def convert_to_link(a_href: str) -> str:
        return a_href.split('/url?q=')[-1]


class RecommendGoods:
    SEARCH_URL = 'https://www.google.com/search'
    SEARCH_GOODS_PARAMS = {'tbm': 'shop'}
    DEFAULT_PARAMS = {'hl': 'ru'}
    DEFAULT_COOKIES = {'CONSENT': 'YES+cb.20220826-07-p0.ru+FX+410'}
    SHOPS_BEFORE_TEXT = 'Купить '
    SHOPS_AFTER_TEXT = ' в Новотроицке | Орске'

    def __init__(self, gift):
        self.gift = gift
        self.write_goods()
        self.write_shops()

    def write_goods(self):
        r = requests.get(
            self.SEARCH_URL,
            params={'q': self.gift, **self.SEARCH_GOODS_PARAMS, **self.DEFAULT_PARAMS},
            cookies=self.DEFAULT_COOKIES
        )
        soup = bs(r.text, 'lxml')
        self.goods = ParseGoods(soup=soup).parsed_goods

    def write_shops(self):
        r = requests.get(
            self.SEARCH_URL,
            params={
                'q': f'{self.SHOPS_BEFORE_TEXT}{self.gift}{self.SHOPS_AFTER_TEXT}', **self.DEFAULT_PARAMS
            },
            cookies=self.DEFAULT_COOKIES
        )
        soup = bs(r.text, 'lxml')
        self.shops = ParseShops(soup=soup).parsed_shops
