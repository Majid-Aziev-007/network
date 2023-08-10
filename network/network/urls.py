from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('meetings.urls', namespace='meetings')),
    path('admin/', admin.site.urls),
]
