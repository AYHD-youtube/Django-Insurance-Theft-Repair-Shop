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
    path('shop/buy/login/register/', views.buy_register, name='shop_buy_register'),
    path('insurance/login/', views.insurance_login, name='insurance_login'),
    path('insurance/login/approve/', views.insurance_approve, name='insurance_approve'),
    path('insurance/login/disapprove/', views.insurance_disapprove, name='insurance_disapprove'),
    path('insurance/login/claim_insurance/', views.claim_insurance, name='claim_insurance'),
    path('insurance/login/claim_insurance/claim_submit/', views.claim_submit, name='claim_submit'),
    path('police/login/', views.police_login, name='police_login'),
    path('police/login/solved/', views.solved, name='solved'),
    path('repair/login/', views.repair_login, name='repair_login'),
    path('repair/login/approved/', views.repair_approved, name='repair_approved'),
    path('repair/login/declined/', views.repair_declined, name='repair_declined'),
    path('police/login/approved/', views.police_approved, name='police_approved'),
    path('police/login/declined/', views.police_declined, name='police_declined'),
]