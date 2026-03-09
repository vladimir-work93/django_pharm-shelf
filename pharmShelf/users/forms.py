from datetime import date

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django import forms
from .models import User, UserMedication
from django.core.exceptions import ValidationError

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

class UserProfileForm(UserChangeForm):
    """Редактирование профиля"""
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'snils')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Иван',
                'id': 'firstName'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Иванов',
                'id': 'lastName'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@mail.ru',
                'id': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+79991234567',
                'id': 'phone'
            }),
            'snils': forms.TextInput(attrs={
                'placeholder': '123-456-789 00',
                'id': 'snils'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('Email уже используется')
        return email

class UserProfileForm(UserChangeForm):
    """Редактирование профиля"""
    password = None

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'snils')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Иван',
                'id': 'firstName'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Иванов',
                'id': 'lastName'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'example@mail.ru',
                'id': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+79991234567',
                'id': 'phone'
            }),
            'snils': forms.TextInput(attrs={
                'placeholder': '123-456-789 00',
                'id': 'snils'
            }),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError('Email уже используется')
        return email

class UserMedicationForm(forms.ModelForm):
    """
    Форма для добавления лекарства в аптечку пользователя
    """

    class Meta:
        model = UserMedication
        fields = ['production_date', 'expiry_date', 'quantity', 'is_searchable']
        widgets = {
            'production_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'ГГГГ-ММ-ДД'
                }
            ),
            'expiry_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'ГГГГ-ММ-ДД'
                }
            ),
            'quantity': forms.TextInput(
                attrs={
                    'class': 'form-control quantity-input',
                    'min': '1',
                    'max': '9999',
                    'value': '1',
                }
            ),
            'is_searchable': forms.CheckboxInput(
                attrs={
                    'class': 'form-checkbox'
                }
            ),
        }
        labels = {
            'production_date': 'Дата производства',
            'expiry_date': 'Годен до',
            'quantity': 'Количество',
            'is_searchable': 'Разрешить поиск'
        }
        help_texts = {
            'production_date': 'Укажите дату производства лекарства',
            'expiry_date': 'Укажите дату истечения срока годности',
            'quantity': 'Укажите количество упаковок (от 1 до 9999)',
            'is_searchable': 'Другие пользователи смогут найти это лекарство в вашей аптечке'
        }

    def clean(self):
        cleaned_data = super().clean()
        production_date = cleaned_data.get('production_date')
        expiry_date = cleaned_data.get('expiry_date')
        today = date.today()

        if not production_date:
            self.add_error('production_date',
                           'Заполните дату производства')

        if not expiry_date:
            self.add_error('expiry_date',
                           'Заполните дату срока годности')

        # Проверка: дата производства не может быть в будущем
        if production_date and production_date > today:
            self.add_error('production_date',
                'Дата производства не может быть в будущем')

        # Проверка: дата производства не может быть позже даты истечения срока
        if production_date and expiry_date and production_date > expiry_date:
            self.add_error('expiry_date',
                'Срок годности не может быть раньше даты производства')

        # Проверка: если срок годности указан, он должен быть в будущем
        if expiry_date and expiry_date < today:
            self.add_error('expiry_date',
                'Нельзя добавить лекарство с истекшим сроком годности')

        return cleaned_data

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity and quantity < 1:
            raise forms.ValidationError('Количество должно быть не менее 1')
        if quantity and quantity > 9999:
            raise forms.ValidationError('Количество не может превышать 9999')
        return quantity