from django.shortcuts import render
from django.core.paginator import Paginator
#from .models import UserMedication, Medication, Manufacturer, ReleaseForm, DosageType


def main_view(request):
    return render(request, 'main/main.html')

def catalog_view(request):
    return render(request, 'main/catalog.html')