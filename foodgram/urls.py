from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apps.main.views import InternalServerError, PageNotFound
from foodgram import settings


handler404 = PageNotFound.as_view()
handler500 = InternalServerError.as_error_view()


urlpatterns = [
    path('', include('apps.main.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('user/', include('apps.users.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
