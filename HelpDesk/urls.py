from django.contrib import admin
from django.urls import include, path
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Main.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('debug/',include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
