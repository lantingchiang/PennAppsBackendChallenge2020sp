from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('api', views.api, name='api'),
    path('api/clubs', views.api_clubs, name='api_clubs'),
    path('api/user/<username>', views.api_user, name='api_user'),
    path('api/favorite', views.api_favorite, name='api_favorite'),
]