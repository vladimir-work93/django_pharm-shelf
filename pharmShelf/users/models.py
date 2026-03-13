from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.validators import EmailValidator
from django.contrib.auth.base_user import BaseUserManager

from main.models import Medication


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
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=20,
        blank=True
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=40,
        blank=True
    )

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

    city = models.CharField(
        max_length=100,
        verbose_name='Город',
        blank=False,
        null=False,
        help_text='Ваш город',
    )

    USERNAME_FIELD = 'email' # Замена поля аутентификации на email
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

class UserMedication(models.Model):
    """Лекарство пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='user_medications',
        db_column='user_id'
    )
    medication = models.ForeignKey(
        Medication,
        on_delete=models.PROTECT,
        related_name='user_medications',
        db_column='medication_id'
    )
    production_date = models.DateField(null=True, blank=True, verbose_name='Дата производства')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='Годен до')
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество',
        validators=[MinValueValidator(1), MaxValueValidator(9999)]
    )
    is_searchable = models.BooleanField(default=False, verbose_name='Доступно для поиска')
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        db_table = 'USER_MEDICATIONS'
        verbose_name = 'Лекарство пользователя'
        verbose_name_plural = 'Лекарства пользователей'

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.medication.name}"

    @property
    def is_expired(self):
        """Проверяет, просрочено ли лекарство"""
        if self.expiry_date:
            return self.expiry_date < date.today()
        return False

    @property
    def is_expiring_soon(self):
        """Проверяет, истекает ли срок годности в ближайшие 30 дней"""
        if self.expiry_date and not self.is_expired:
            days_until_expiry = (self.expiry_date - date.today()).days
            return 0 <= days_until_expiry <= 30
        return False