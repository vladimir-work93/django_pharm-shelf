from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import User

class UserLoginForm(AuthenticationForm):
    # Переопределение формы username
    username = forms.EmailField(
        label = 'Электронная почта',
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'id': 'loginEmail',
            'name': 'email',
            'placeholder': 'example@mail.ru',
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'id': 'loginPassword',
            'name': 'password',
            'placeholder': 'Введите пароль'
        })
    )
    class Meta:
        model = User
        fields = ('email', 'password')

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'id': 'firstName',
            'name': 'first_name',
            'placeholder': 'Иван'
        })
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'id': 'lastName',
            'name': 'last_name',
            'placeholder': 'Иванов'
        })
    )
    email = forms.EmailField(
        label = 'Электронная почта',
        widget=forms.EmailInput(attrs={
            'id': 'registerEmail',
            'name': 'email',
            'placeholder': 'example@mail.ru',
        })
    )
    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'id': 'phone',
            'name': 'phone',
            'placeholder': '+71112223344'
        })
    )
    snils = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'id': 'snils',
            'name': 'snils',
            'placeholder': '123-456-789 00'
        })
    )
    password1 = forms.CharField(
        label='Пароль-1',
        widget=forms.PasswordInput(attrs={
            'id': 'registerPassword',
            'name': 'password',
            'placeholder': 'Минимум 8 символов'
        })
    )
    password2 = forms.CharField(
        label='Пароль-2',
        widget=forms.PasswordInput(attrs={
            'id': 'confirmPassword',
            'name': 'confirm_password',
            'placeholder': 'Введите пароль еще раз'
        })
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'snils', 'password1', 'password2')
