from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm
from django.contrib import auth, messages


# Create your views here.

def login_view(request):
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