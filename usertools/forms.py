from django.contrib.auth.forms import UserCreationForm

from usertools.models import BaseUser


class RegisterForm(UserCreationForm):

    class Meta:
        model = BaseUser
        fields = ('email', 'phone', 'first_name', 'last_name', 'password1', 'password2')


# class RegisterForm(forms.ModelForm):
#     first_name = forms.CharField(label='Имя')
#     last_name = forms.CharField(label='Фамилия')
#     email = forms.EmailField(label='Введите email')
#     phone = forms.CharField(label='Введите телефон')
#     password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
#     password_repeat = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
#
#     def clean(self):
#         self.validate_password()
#         clean_first_name = self.cleaned_data['first_name'].replace(' ', '')
#         clean_last_name = self.cleaned_data['last_name'].replace(' ', '')
#         clean_username = (
#             f"{clean_first_name}{clean_last_name}"
#         )
#         if re.match(r'\W', clean_username):
#             raise ValidationError('Имя и Фамилия должны содержать тольок буквенные символы')
#         elif re.findall(r'[а-я]+', clean_username.lower())[0] != clean_username.lower():
#             raise ValidationError('Имя и Фамили должны содержать только символы кирилицы')
#
#         self.cleaned_data['username'] = clean_username
#         self.cleaned_data.pop('last_name')
#         self.cleaned_data.pop('first_name')
#         self.cleaned_data.pop('password_repeat')
#
#         return self.cleaned_data
#
#     def validate_password(self):
#         password = self.cleaned_data['password']
#         has_upper_case = password.lower() != password
#
#         if not self.cleaned_data['password'] == self.cleaned_data['password_repeat']:
#             raise ValidationError('Пароли не совпадают')
#         elif (len(self.cleaned_data['password']) < 8) or has_upper_case or re.match(r'\w', password):
#             return ValidationError(
#                 'Парль должен быть 8 или более символов, содержать мадые и заглавне буквы'
#             )
