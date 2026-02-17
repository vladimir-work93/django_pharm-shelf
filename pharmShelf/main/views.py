from django.shortcuts import render


def main_view(request):
    return render(request, 'main/main.html')

def catalog_view(request):
    return render(request, 'main/catalog.html')