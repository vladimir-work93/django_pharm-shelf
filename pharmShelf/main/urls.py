from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('users/', include('users.urls')),
]