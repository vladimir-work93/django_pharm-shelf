from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.main_view, name='main'),
    path('catalog/', views.catalog_view, name='catalog'),
]