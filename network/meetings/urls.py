from django.urls import path

from . import views

app_name = 'meetings'

urlpatterns = [
    path('', views.index, name='index'),
    path('topic/<slug:slug>/', views.topic_meetings, name='topic_list'),
    path('meetings/<int:meeting_id>/', views.meeting_detail, name='meeting_detail'),
    path('meetings/create/', views.meeting_create, name='meeting_create'),
    path(
        'meetings/<int:meeting_id>/presence/',
        views.meeting_presence,
        name='meeting_presence'
    ),
    path(
        'meetings/<int:meeting_id>/not_presence/',
        views.meeting_not_presence,
        name='meeting_not_presence'
    ),
    path('page-buy/<int:meeting_id>/', views.page_buy, name='page_buy'),
    path('buy-check/<int:meeting_id>/', views.buy_check, name='buy_check'),
]
