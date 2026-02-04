from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    # path('catalog/', views.catalog_view, name='catalog'),
    # path('my-shelf/', views.my_shelf_view, name='my_shelf'),
    # path('add/', views.add_medication_view, name='add'),
    # path('profile/', views.profile_view, name='profile'),
    path('login/', include('users.urls')),
    # path('logout/', views.logout_view, name='logout'),
    # path('register/', views.register_view, name='register'),
]