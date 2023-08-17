from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('meetings.urls', namespace='meetings')),
    path('profile/', include('customers.urls', namespace='customers')),
    path('sub/', include('subscription.urls', namespace='subscription')),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]
