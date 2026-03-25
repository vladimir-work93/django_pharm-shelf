from django.shortcuts import render
from .models import Medication


def main_view(request):
    return render(request, 'main/main.html')