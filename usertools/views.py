from django.contrib.auth import logout, login, get_user_model
from django.contrib.auth.models import Permission
from django.db.models import Count
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import CreateView, View, DetailView
from django.contrib.auth.views import LoginView, AuthenticationForm
from django.shortcuts import redirect, render
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.exceptions import ValidationError

from letters.models import Letter, Gift

from .utils import DbToExcel, ConfirmEmailMixin, RecommendGoods
from .forms import RegisterForm

from wishtree.settings.settings import BASE_DIR


User = get_user_model()


# Auth views
class LoginPage(LoginView, ConfirmEmailMixin):
    form_class = AuthenticationForm
    template_name = 'usertools/login.html'

    def form_valid(self, form):
        user = form.get_user()

        if not user.email_is_verified:
            self.send_confirm_email(user)
            return redirect('usertools:email_was_send')

        login(self.request, user)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


class RegisterView(CreateView, ConfirmEmailMixin):
    form_class = RegisterForm
    template_name = 'usertools/register.html'

    def form_valid(self, form):
        user = form.save()
        self.send_confirm_email(user)
        return redirect('usertools:email_was_send')


class ConfirmEmail(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if not (user is not None and token_generator.check_token(user, token)):
            raise Http404('Данные для подтверждения email оказались неверны, попробуйте войти снова')
            
        user.email_is_verified = True
        user.save()
        login(request, user)
        response = redirect('index')

        return response

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                User.DoesNotExist, ValidationError):
            user = None
        return user
# End auth views


def email_was_send(request):
    return render(request, 'usertools/email_was_send.html')


def user_selected(request):
    context = {}

    if request.user.is_authenticated:
        letters = Letter.objects.filter(
            picked_by=request.user
        ).prefetch_related('gift').prefetch_related('child')

        if letters.exists():
            context['letters'] = letters
        else:
            context['empty_object_text'] = 'info/need_select_selected.html'
    else:
        context['empty_object_text'] = 'info/need_login.html'

    return render(request, 'usertools/selected_gifts.html', context)


# admin views
class AdminPageLetters(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponse(status=403)

        ordering = self.kwargs['ordering']
        letters = Letter.objects.all()
        if not ordering == 'all':
            letters = letters.filter(gift__status=Gift.GIFT_STATUS_CHOICES[int(ordering)][0])

        return render(request, 'usertools/admin_letters.html', {'letters': letters, 'ordering': ordering})


class AdminPageUsers(View):

    @staticmethod
    def get(request):
        if not request.user.is_staff:
            return HttpResponse(status=403)

        users = User.objects.filter(letters__isnull=False).annotate(
            num_letters=Count('letters')
        ).order_by('-num_letters')

        return render(request, 'usertools/admin_users.html', {'users': users})


def clear_user_letters(request, pk):
    if not request.user.is_staff:
        return HttpResponse(status=403)

    user = User.objects.get(pk=pk)
    user.letters.set([])
    cannot_select_letters = Permission.objects.get(codename='cannot_select_letters')
    user.user_permissions.add(cannot_select_letters)

    return redirect('usertools:admin_users')
# end admin views


def update_gift(request, gift_id, status):
    status = Gift.GIFT_STATUS_CHOICES[int(status)][0]
    gift = Gift.objects.filter(pk=gift_id)

    if status == 'unselect':
        Letter.objects.filter(gift=gift.first()).update(picked_by=None)

    gift.update(status=status)
    return HttpResponse(status=200)


def add_favorite(request, pk):
    if request.user.has_perm('usertools.cannot_select_letters'):
        return HttpResponse('cannot_select_letters', status=403)

    if not request.user.is_authenticated:
        return redirect('usertools:login')

    if request.user.letters.exists():
        return redirect('usertools:favorites')

    letter = Letter.objects.get(pk=pk, gift__status='unselect')
    request.user.favorites.add(letter.pk)

    return HttpResponse(status=200)


def remove_list_favorites(request, favorites):
    clean_favorites = favorites.strip().split(',')
    # check if letter not have in user favorites
    for letter in clean_favorites:
        request.user.favorites.remove(letter)

    return HttpResponse(status=200)


def favorites_to_selected(request, favorites):
    favorites = favorites.strip().split(',')

    request.user.letters.set(Letter.objects.filter(pk__in=favorites))
    for letter in request.user.letters.prefetch_related('gift'):
        letter.gift.status = 'selected'

    request.user.favorites.set([])
    request.user.save()

    return redirect('usertools:user_selected')


def db_to_excel(request):
    if not request.user.is_superuser:
        return HttpResponse(status=403)

    excel_file = BASE_DIR / 'media' / 'excel' / 'excel_table.xlsx'
    DbToExcel().write_to_excel(excel_file)

    with excel_file.open('rb') as f:
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'inline; filename=excel_table.xlsx'
        return response


def favorite_page(request):
    context = {}
    if not request.user.is_authenticated:
        context['empty_object_text'] = 'info/need_login.html'
    else:
        favorites = request.user.favorites
        if favorites.exists():
            context['letters'] = favorites
        else:
            if request.user.letters.exists():
                context['empty_object_text'] = 'info/already_select.html'
            else:
                context['empty_object_text'] = 'info/need_select_favorites.html'

    return render(request, 'usertools/favorites.html', context)


class RecommendGoodsView(DetailView):
    model = Gift
    template_name = 'usertools/recommend.html'
    pk_url_kwarg = 'gift_pk'
    context_object_name = 'gift'


def get_recommend_goods(request, pk):
    gift = Gift.objects.get(pk=pk)
    dependency = RecommendGoods(gift=gift.name)
    print(type(dependency.shops))
    print(type(dependency.goods))
    return JsonResponse({'goods': dependency.goods, 'shops': dependency.shops})
