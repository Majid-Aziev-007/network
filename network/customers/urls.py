from django.urls import path

from . import views

app_name = 'customers'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('key-valid/', views.key_valid, name='key_valid'),
    path('key-valid/<int:key_input>/', views.key_valid, name='key_valid'),
]
