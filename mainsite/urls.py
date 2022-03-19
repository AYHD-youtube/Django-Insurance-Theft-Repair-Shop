from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/', views.shop, name='shop'),
    path('insurance/', views.insurance, name='insurance'),
    path('police/', views.police, name='police'),
    path('repair/', views.repair, name='repair'),
    path('shop/buy/', views.buy, name='buy'),
    path('shop/buy/login/', views.buy_login, name='shop_buy_login'),
    path('insurance/login/', views.insurance_login, name='insurance_login'),
    path('insurance/login/claim_insurance/', views.claim_insurance, name='claim_insurance'),
    path('insurance/login/claim_insurance/claim_submit/', views.claim_submit, name='claim_submit'),
]