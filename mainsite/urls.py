from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('insurance/', views.insurance, name='insurance'),
    path('police/', views.police, name='police'),
    path('repair/', views.repair, name='repair'),
]