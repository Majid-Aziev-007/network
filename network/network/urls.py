from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = 'core.views.page_not_found'
handler500 = 'core.views.server_error'

urlpatterns = [
    path('', include('meetings.urls', namespace='meetings')),
    path('profile/', include('customers.urls', namespace='customers')),
    path('auth/', include('users.urls')),
    path('panel-creator/', include('panelcreator.urls', namespace='panelcreator')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
