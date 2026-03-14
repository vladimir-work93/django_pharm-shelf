from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot_password/', views.forgot_password_view, name='forgot_password'),

    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:section>/', views.profile_section, name='profile_section'),

    path('password-change/', views.CustomPasswordChangeView.as_view(), name='password_change'),

    path('add-to-chest/<int:medication_id>/', views.add_to_medicine_chest, name='add_to_medicine_chest'),

    path('medication/<int:pk>/edit/', views.medication_edit_view, name='medication_edit'),
    path('medication/<int:pk>/delete/', views.medication_delete_view, name='medication_delete'),
    path('medication/<int:pk>/make-searchable/', views.make_medication_searchable, name='medication_make_searchable'),

    path('search-medications/', views.search_user_medications_view, name='search_user_medications'),

]