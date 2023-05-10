from django.urls import path
from rest_framework.authtoken import views

from .views import (friend_request, friend_request_list, friends,
                    friendship_status, register)

app_name = 'users'

urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/register/', register, name='register'),
    path('v1/friends/', friends, name='friends'),
    path('v1/friends/<slug:username>/', friends, name='friends-detail'),
    path(
        'v1/friendship/request/<slug:username>/',
        friend_request, name='friends-request-type'
        ),
    path(
        'v1/friendship/request/list/<slug:rtype>/',
        friend_request_list,
        name='friends-request-list'
        ),
    path(
        'v1/friendship/status/<slug:username>/',
        friendship_status,
        name='friendship-status'),
]
