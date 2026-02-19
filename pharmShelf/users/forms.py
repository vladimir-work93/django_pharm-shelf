from django.contrib.auth.forms import AuthenticationForm
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