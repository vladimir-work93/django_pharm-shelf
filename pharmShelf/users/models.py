from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractUser):
    phone_validator = RegexValidator(
        regex=r'^\+7\d{10}$',
        message='Телефон должен быть в формате: +79991234567'
    )

    snils_validator = RegexValidator(
        regex=r'^\d{3}-\d{3}-\d{3} \d{2}$',
        message='СНИЛС должен быть в формате: ХХХ-ХХХ-ХХХ ХХ'
    )

    phone = models.CharField(
        max_length=12,  # РФ номер: +7XXXXXXXXXX (12 символов с плюсом)
        verbose_name='Телефон',
        unique=True,  # Обычно телефон должен быть уникальным
        blank=False,  # Явно указываем, что поле не может быть пустым в формах
        null=False,  # В базе данных NOT NULL
        help_text = 'Формат: +7XXXXXXXXXX',  # Подсказка для пользователя
        default='+70000000000',  # Значение по умолчанию
        validators = [phone_validator],
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
