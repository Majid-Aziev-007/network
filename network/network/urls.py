from django.contrib import admin
from django.urls import include, path

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

urlpatterns = [
    path('', include('meetings.urls', namespace='meetings')),
    path('profile/', include('customers.urls', namespace='customers')),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
]
