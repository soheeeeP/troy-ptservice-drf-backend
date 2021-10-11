"""Troy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt import authentication

import debug_toolbar
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    info=openapi.Info(
        title='Troy backend API',
        default_version='v1',
        description='Troy 서비스 백엔드 API 문서',
        contact=openapi.Contact(email='mtom.troy21@gmail.com'),
        license=openapi.License(name='M-TO-M License'),
    ),
    public=True,
    authentication_classes=(authentication.JWTAuthentication,),
    permission_classes=(permissions.AllowAny,),
)


class HealthCheckAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(data={"status": "ok"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path("health/", HealthCheckAPIView.as_view(), name="health-check"),
    path('troy/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('troy/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.IS_DEBUG_MODE is True:
    urlpatterns += [
        path('debug/', include(debug_toolbar.urls)),
    ]
