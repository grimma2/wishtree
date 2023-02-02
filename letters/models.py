from django.db import models
from django.urls import reverse

from wishtree.settings import AUTH_USER_MODEL


class Child(models.Model):
    name = models.CharField('Имя', max_length=255)
    age = models.PositiveSmallIntegerField('Возвраст')

    def __str__(self):
        return self.name

    def get_full_name(self) -> str:
        return f'{self.name}, {self.age} лет'

    class Meta:
        verbose_name = 'Ребёнок'
        verbose_name_plural = 'Дети'


class Gift(models.Model):

    UN = 'unselect'
    S = 'selected'
    DEL = 'delivered'

    GIFT_STATUS_CHOICES = [
        (UN, 'Ещё не выбрано'),
        (S, 'Выбрано'),
        (DEL, 'Доставлено')
    ]

    name = models.CharField('Название подарка', max_length=99)
    status = models.CharField('Состояние подарка', max_length=99, choices=GIFT_STATUS_CHOICES, default=UN)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подарок'
        verbose_name_plural = 'Подарки'


class Letter(models.Model):
    picked_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='letters', null=True, blank=True
    )
    favorite_select = models.ManyToManyField(AUTH_USER_MODEL, related_name='favorites', blank=True)
    child = models.OneToOneField(Child, on_delete=models.CASCADE, null=True, blank=True)
    gift = models.OneToOneField(Gift, on_delete=models.PROTECT)
    photo = models.FileField('Письмо', upload_to='images/letter/')

    def get_user_to_excel(self):
        full_name = self.picked_by.get_full_name()
        phone = self.picked_by.phone or ''
        email = self.picked_by.email

        return {'email': email, 'full_name': full_name, 'phone': phone}

    def __str__(self):
        return f'Письмо номер {self.pk}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'
