from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),
]