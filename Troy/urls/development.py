import debug_toolbar

from .base import *
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += [
    path('debug/', include(debug_toolbar.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)