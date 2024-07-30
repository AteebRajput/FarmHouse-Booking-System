from django.urls import path
from . import views

urlpatterns = [
    path('', views.farm_list, name='farm_list'),
    path('farm/<int:farm_id>/', views.farm_detail, name='farm_detail'),
    path('farm/<int:farm_id>/book/', views.book_farm, name='book_farm'),
     
]
