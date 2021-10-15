from django.urls import include, path


urlpatterns = [
    path('users/', include('api.users.urls')),
    path('oauth/', include('api.oauth.urls')),
    path('programs/', include('api.programs.urls')),
    path('verify/', include('api.verify.urls')),
]
