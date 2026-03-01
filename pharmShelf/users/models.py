from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import EmailValidator
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей, где email используется как уникальный идентификатор
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя
        """
        if not email:
            raise ValueError('Email должен быть указан')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    phone_validator = RegexValidator(
        regex=r'^\+7\d{10}$',
        message='Телефон должен быть в формате: +79991234567'
    )

    snils_validator = RegexValidator(
        regex=r'^\d{3}-\d{3}-\d{3} \d{2}$',
        message='СНИЛС должен быть в формате: ХХХ-ХХХ-ХХХ ХХ'
    )

    username = None

    email = models.EmailField(
        max_length=254,
        verbose_name='Электронная почта',
        unique=True,
        blank=False,
        null=False,
        help_text='Формат: example@mail.ru',
        default='example@mail.ru',
        validators=[EmailValidator()],
    )

    phone = models.CharField(
        max_length=12,  # РФ номер: +7XXXXXXXXXX (12 символов с плюсом)
        verbose_name='Телефон',
        unique=True,  # Обычно телефон должен быть уникальным
        blank=False,  # Явно указываем, что поле не может быть пустым в формах
        null=False,  # В базе данных NOT NULL
        help_text='Формат: +7XXXXXXXXXX',  # Подсказка для пользователя
        default='+70000000000',  # Значение по умолчанию
        validators=[phone_validator],
    )

    snils = models.CharField(
        max_length=14,  # СНИЛС: ХХХ-ХХХ-ХХХ ХХ (14 символов с дефисами и пробелом)
        verbose_name='СНИЛС',
        unique=True,  # СНИЛС должен быть уникальным
        blank=False,
        null=False,
        help_text='Формат: ХХХ-ХХХ-ХХХ ХХ',  # Подсказка для пользователя
        default='000-000-000 00',  # Значение по умолчанию
        validators=[snils_validator],
    )

    USERNAME_FIELD = 'email' # Замена поля аутентификации на email
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
