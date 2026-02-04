from django.shortcuts import render
from django.core.paginator import Paginator
#from .models import UserMedication, Medication, Manufacturer, ReleaseForm, DosageType


def main_view(request):
    return render(request, 'main/main.html')

# def catalog_view(request):
#     # Получаем только лекарства, доступные для поиска
#     medications_list = UserMedication.objects.filter(
#         is_searchable=True
#     ).select_related(
#         'user',
#         'medication',
#         'medication__manufacturer',
#         'medication__release_form',
#         'medication__dosage_type'
#     ).order_by('-expiry_date')
#
#     # Пагинация
#     paginator = Paginator(medications_list, 12)  # 12 карточек на странице
#     page = request.GET.get('page')
#     medications = paginator.get_page(page)
#
#     return render(request, 'main/catalog.html', {
#         'user_medications': medications,
#         'title': 'Каталог лекарств'
#     })