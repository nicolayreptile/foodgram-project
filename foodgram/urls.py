from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from foodgram import settings


handler404 = 'apps.main.error_handlers.page_not_found'
handler500 = 'apps.main.error_handlers.server_error'


urlpatterns = [
    path('', include('apps.main.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('user/', include('apps.users.urls')),
    path('/', include('django.contrib.flatpages.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
