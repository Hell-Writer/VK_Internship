from django.urls import path, include
from .views import UserViewSet, register, follow, friends, friend_request, friendship_status
from rest_framework import routers
from rest_framework.authtoken import views

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/register/', register, name='register'),
    path('v1/follow/', follow, name='follow'),
    path('v1/friends/', friends, name='friends'),
    path('v1/friendship_request/', friend_request, name='friend_request'),
    path('v1/friendship_status/', friendship_status, name='friendship_status'),
]
