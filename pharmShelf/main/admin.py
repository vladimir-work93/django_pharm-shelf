from django.contrib import admin
from .models import Manufacturer, Medication

# Register your models here.

admin.site.register(Manufacturer)
admin.site.register(Medication)