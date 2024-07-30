# admin_interface/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('farms/', views.admin_farm_list, name='admin_farm_list'),
    path('farms/<int:pk>/', views.admin_farm_detail, name='admin_farm_detail'),
    path('farms/<int:pk>/delete/', views.admin_delete_farm, name='admin_delete_farm'),
    path('farms/<int:pk>/update/', views.admin_update_farm, name='admin_update_farm'),
    path('users/', views.admin_user_list, name='admin_user_list'),
    path('users/<int:pk>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('users/<int:pk>/update/', views.admin_update_user, name='admin_update_user'),
    path('bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('bookings/<int:pk>/cancel/', views.admin_cancel_booking, name='admin_cancel_booking'),
    path('register_farm/', views.register_farm, name='register_farm'),
    path('register_user/',views.register_page,name="register_user"),
    path('create_booking/', views.admin_create_booking, name='admin_create_booking'),

]
