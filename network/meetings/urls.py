from django.urls import path

from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.index, name='index'),
    path('topic/<slug:slug>/', views.topic_meetings, name='topic_list'),
    path('meetings/<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
]
