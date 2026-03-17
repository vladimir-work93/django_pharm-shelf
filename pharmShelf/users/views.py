from datetime import date, timedelta

from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView

from django.core.paginator import Paginator

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserMedicationForm

from .models import UserMedication, User
from main.models import Medication

from django.db.models import Q


# Create your views here.

def login_view(request):
    # Проверяем, авторизован ли пользователь
    if request.user.is_authenticated:
        # Если авторизован, перенаправляем на страницу профиля с разделом my_medicines
        return redirect('users:profile_section', section='my_medicines')

    if request.method == 'POST':
        data = request.POST
        form = UserLoginForm(data=data)
        if form.is_valid():
            email = data['username']
            password = data['password']
            user = auth.authenticate(email=email, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('main:main')
    else:
        form = UserLoginForm()

    context = {
        'form': form
    }

    return render(request, 'users/login.html', context)

def register_view(request):
    if request.method == 'POST':
        data = request.POST
        form = UserRegisterForm(data=data)
        if form.is_valid():
            form.save()
            messages.success(request, message='Вы успешно зарегистрировались!')
            return redirect('users:login')
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()

    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)

def logout_view(request):
    auth.logout(request)
    return redirect('main:main')

def forgot_password_view(request):
    return render(request, 'users/forgot_password.html')

@login_required
def profile_view(request):
    """Страница профиля с аптечкой"""
    # Перенаправляем на основной профиль с аптечкой
    return redirect('users:profile_section', section='my_profile')

@login_required
def edit_profile_view(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('users:profile_section', section='my_profile')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'form': form
    }

    return render(request, 'users/edit_profile.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    """Смена пароля"""
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        messages.success(self.request, 'Пароль успешно изменен!')
        return super().form_valid(form)

@login_required
def add_to_medicine_chest(request, medication_id):
    """
    Представление для добавления лекарства в аптечку пользователя
    """
    medication = get_object_or_404(Medication, id=medication_id)

    if request.method == 'POST':
        form = UserMedicationForm(request.POST)
        if form.is_valid():
            user_medication = form.save(commit=False)
            user_medication.user = request.user
            user_medication.medication = medication
            user_medication.save()

            messages.success(request, f'Лекарство "{medication.name}" успешно добавлено в аптечку')
            return redirect('users:profile_section', section='my_medicines')
    else:
        form = UserMedicationForm(initial={'medication': medication})

    return render(request, 'users/medication_add.html', {
        'form': form,
        'medication': medication
    })

@login_required
def medication_edit_view(request, pk):
    """Редактирование лекарства в аптечке"""
    med_item = get_object_or_404(UserMedication, pk=pk, user=request.user)

    if request.method == 'POST':
        form = UserMedicationForm(request.POST, instance=med_item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Запись обновлена!')
            return redirect('users:profile_section', section='my_medicines')
    else:
        form = UserMedicationForm(instance=med_item)

    return render(request, 'users/medication_edit.html', {
        'form': form,
        'medication': med_item.medication,
        'user_medication': med_item
    })

@login_required
def medication_delete_view(request, pk):
    """Удаление лекарства из аптечки"""
    med_item = get_object_or_404(UserMedication, pk=pk, user=request.user)

    if request.method == 'POST':
        med_item.delete()
        messages.success(request, 'Лекарство удалено из аптечки')
        return redirect('users:profile_section', section='my_medicines')

    return render(request, 'users/medication_confirm_delete.html', {
        'med_item': med_item
    })

@login_required
def make_medication_searchable(request, pk):
    """
    Делает лекарство доступным для поиска
    """
    # Получаем лекарство пользователя, проверяем что оно принадлежит текущему пользователю
    medication = get_object_or_404(UserMedication, pk=pk, user=request.user)

    # Проверяем условие: только если скоро истекает и еще не доступно для поиска
    if medication.is_expiring_soon and not medication.is_searchable:
        medication.is_searchable = True
        medication.save()
        messages.success(request, f'Лекарство "{medication.medication.name}" теперь доступно для поиска.')
    else:
        messages.error(request, 'Нельзя сделать это лекарство доступным для поиска.')

    # Перенаправляем обратно на страницу со списком лекарств
    return redirect('users:profile_section', section='my_medicines')

def search_user_medications_view(request):
    """
    Поиск лекарств среди всех пользователей
    """
    # Базовый запрос: все лекарства пользователей, доступные для поиска
    medications = UserMedication.objects.filter(
        is_searchable=True,  # Только те, что разрешены для поиска
        user__isnull = False  # Если нужно проверить, что пользователь существует
    )
    # Исключаем лекарства текущего пользователя только если он авторизован
    if request.user.is_authenticated:
        medications = medications.exclude(user=request.user)

    medications = medications.select_related(
        'user',
        'medication',
        'medication__manufacturer'
    ).order_by('-added_at')

    # Поиск по названию лекарства
    search_query = request.GET.get('search', '')
    if search_query:
        medications = medications.filter(
            Q(medication__name__icontains=search_query) |
            Q(medication__name__icontains=search_query.lower()) |
            Q(medication__name__icontains=search_query.upper()) |
            Q(medication__name__icontains=search_query.capitalize())
        ).distinct()

    # Сортировка
    sort_by = request.GET.get('sort', 'date')
    sort_direction = request.GET.get('direction', 'desc')

    sort_field_map = {
        'name': 'medication__name',
        'user': 'user__email',
        'date': 'added_at',
        'expiry': 'expiry_date',
    }

    sort_field = sort_field_map.get(sort_by, 'added_at')
    if sort_direction == 'desc':
        sort_field = f'-{sort_field}'

    medications = medications.order_by(sort_field)

    # Пагинация
    paginator = Paginator(medications, 10)  # 10 элементов на страницу
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'medications': page_obj,
        'search_query': search_query,
        'current_sort': sort_by,
        'current_direction': sort_direction,
    }

    return render(request, 'users/search_user_medications.html', context)

@login_required
def profile_section(request, section):
    """
    Отображает разные разделы профиля
    """

    # Базовая информация о пользователе
    context = {
        'user': request.user,
        'section': section,  # Для подсветки активного пункта меню
    }

    # Дополнительные данные в зависимости от раздела
    if section == 'my_profile':
        # Статистика для профиля
        medicines_count = UserMedication.objects.filter(user=request.user).count()
        expiring_count = UserMedication.objects.filter(
            user=request.user,
            expiry_date__lte=date.today() + timedelta(days=30),
            expiry_date__gte=date.today()
        ).count()
        expired_count = UserMedication.objects.filter(
            user=request.user,
            expiry_date__lt=date.today()
        ).count()

        context.update({
            'medicines_count': medicines_count,
            'expiring_count': expiring_count,
            'expired_count': expired_count,
            'notifications_count': 0,
        })
        template = 'users/my_profile.html'

    elif section == 'edit_profile':
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('users:profile_section', section='my_profile')
        else:
            form = UserProfileForm(instance=request.user)

        context['form'] = form
        template = 'users/edit_profile.html'

    elif section == 'my_medicines':
        # Получаем все лекарства пользователя
        medicines = UserMedication.objects.filter(
            user=request.user
        ).select_related(
            'medication',
            'medication__manufacturer'
        )

        # Поиск по названию лекарства (регистронезависимый)
        search_query = request.GET.get('search', '')
        if search_query:
            # Создаем запрос с разными вариантами регистра
            medicines = medicines.filter(
                Q(medication__name__icontains=search_query) |
                Q(medication__name__icontains=search_query.lower()) |
                Q(medication__name__icontains=search_query.upper()) |
                Q(medication__name__icontains=search_query.capitalize())
            ).distinct()
        context['search_query'] = search_query

        # Сортировка
        sort_by = request.GET.get('sort', 'name')
        sort_direction = request.GET.get('direction', 'asc')

        # Определяем поле для сортировки
        sort_field = 'medication__name'  # по умолчанию
        if sort_by == 'production_date':
            sort_field = 'production_date'
        elif sort_by == 'expiry_date':
            sort_field = 'expiry_date'
        elif sort_by == 'name':
            sort_field = 'medication__name'

        # Применяем направление сортировки
        if sort_direction == 'desc':
            sort_field = f'-{sort_field}'

        medicines = medicines.order_by(sort_field)

        # Сохраняем параметры сортировки для шаблона
        context['current_sort'] = sort_by
        context['current_direction'] = sort_direction

        # Пагинация
        paginator = Paginator(medicines, 5)  # 10 элементов на страницу
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context['page_obj'] = page_obj
        context['medicines'] = page_obj  # для обратной совместимости

        template = 'users/my_medicines.html'


    elif section == 'catalog':

        # Получаем все лекарства из каталога
        medications = Medication.objects.select_related('manufacturer').all()

        # Поиск по названию лекарства (регистронезависимый)
        search_query = request.GET.get('search', '')
        if search_query:
            # Создаем запрос с разными вариантами регистра
            medications = medications.filter(
                Q(name__icontains=search_query) |
                Q(name__icontains=search_query.lower()) |
                Q(name__icontains=search_query.upper()) |
                Q(name__icontains=search_query.capitalize())
            ).distinct()
        context['search_query'] = search_query

        # Пагинация: 6 элементов на страницу (сетка 3x2)
        paginator = Paginator(medications, 6)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['medications'] = page_obj  # для обратной совместимости с шаблоном
        template = 'users/catalog.html'

    elif section == 'search_user_medications':
        search_user_medications_view(request)

    else:
        template = 'users/my_profile.html'

    return render(request, template, context)