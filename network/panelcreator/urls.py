from django.urls import path

from . import views

app_name = 'panelcreator'

urlpatterns = [
    path('', views.panel, name='panel'),
]
