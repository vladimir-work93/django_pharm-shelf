from django.db import models

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Производитель',
    )
    country = models.CharField(
        max_length=100,
        verbose_name='Страна',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'


class Medication(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name = 'Название',
    )
    type = models.CharField(
        max_length=100,
        verbose_name='Тип',
    )
    image_url = models.ImageField(
        verbose_name='Изображение',
        null=True,
        blank=True,
        upload_to='medications/'
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name='medications',
        verbose_name='Производитель',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Лекарство'
        verbose_name_plural = 'Лекарства'