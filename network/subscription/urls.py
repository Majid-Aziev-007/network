from django.urls import path

from . import views

app_name = 'subscription'

urlpatterns = [
    path('page-buy/', views.page_buy, name='page_buy'),
    path('buy-check/', views.buy_check, name='buy_check'),
]
