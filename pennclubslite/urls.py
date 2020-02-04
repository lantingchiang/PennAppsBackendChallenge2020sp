from django.urls import path
from . import views

urlpatterns = [
    # home page
    path('', views.index, name='home'),

    # api endpoints
    path('api/clubs/', views.view_clubs, name='api_clubs'),
    path('api/user/<str:username>/', views.api_user, name='api_user'),
    path('api/favorite/', views.api_favorite, name='api_favorite'),
    path('api/comment/', views.api_comment, name='api_comment'),

]