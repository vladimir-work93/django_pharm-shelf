from django.shortcuts import render
from .models import Medication


def main_view(request):
    return render(request, 'main/main.html')

def catalog_view(request):
    context = {
        'medications': Medication.objects.select_related('manufacturer').all(),
    }
    return render(request, 'main/catalog.html', context)