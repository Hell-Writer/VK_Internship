from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import FRequest, Friendship, User
from .serializers import (FRequestSerializer, FriendshipSerializer,
                          UserSerializer)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def friends(request, username=None):
    user = request.user
    if request.method == "GET":
        friends = Friendship.objects.filter(user_1=user)
        serializer = FriendshipSerializer(friends, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == "DELETE" and username:
        friend = get_object_or_404(User, username=username)
        if Friendship.objects.filter(user_1=user, user_2=friend).exists():
            Friendship.objects.filter(user_1=user, user_2=friend).delete()
            Friendship.objects.filter(user_2=user, user_1=friend).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data=[
                    {'message':
                     'Could not find this person in your friend list'}
                    ], status=status.HTTP_404_NOT_FOUND
            )
    return Response(
        data=[{'message': 'Provide username in Delete method'}],
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friend_request_list(request, rtype='incoming'):
    user = request.user
    if request.method == "GET":
        if rtype == 'incoming':
            frequests = FRequest.objects.filter(reciever=user)
            serializer = FRequestSerializer(frequests, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        if rtype == 'outcoming':
            frequests = FRequest.objects.filter(giver=user)
            serializer = FRequestSerializer(frequests, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(
            data=[{'message': 'Wrong type'}],
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def friend_request(request, username=None):
    user = request.user
    if request.method == "POST":
        FRgiver = get_object_or_404(User, username=username)
        if request.data.get("type") == 'accept':
            frequest = get_object_or_404(
                FRequest,
                reciever=user,
                giver=FRgiver
            )
            frequest.delete()
            Friendship.objects.create(user_1=user, user_2=FRgiver)
            Friendship.objects.create(user_2=user, user_1=FRgiver)
        elif request.data.get("type") == 'decline':
            frequest = get_object_or_404(
                FRequest,
                reciever=user,
                giver=FRgiver
            )
            frequest.delete()
        elif request.data.get("type") == 'send':
            if FRequest.objects.filter(reciever=user, giver=FRgiver).exists():
                FRequest.objects.filter(reciever=user, giver=FRgiver).delete()
                Friendship.objects.create(user_1=user, user_2=FRgiver)
                Friendship.objects.create(user_2=user, user_1=FRgiver)
            else:
                FRequest.objects.create(giver=user, reciever=FRgiver)
        else:
            return Response(
                data=[{'message': 'Wrong type'}],
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(status=status.HTTP_200_OK)
    if request.method == "DELETE" and username:
        FRreciever = get_object_or_404(User, username=username)
        if FRequest.objects.filter(giver=user, reciever=FRreciever).exists():
            FRequest.objects.filter(giver=user, reciever=FRreciever).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                data=[
                    {'message': 'Could not find friend request to given user'}
                    ],
                status=status.HTTP_404_NOT_FOUND
            )
    return Response(
        data=[{'message': 'Provide username in Delete method'}],
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friendship_status(request, username=None):
    user = request.user
    person = get_object_or_404(User, username=username)
    if Friendship.objects.filter(user_1=user, user_2=person).exists():
        return Response(data=[{'status': 'Friend'}], status=status.HTTP_200_OK)
    elif FRequest.objects.filter(giver=user, reciever=person).exists():
        return Response(
            data=[{'status': 'Outcoming friendship request'}],
            status=status.HTTP_200_OK
        )
    elif FRequest.objects.filter(reciever=user, giver=person).exists():
        return Response(
            data=[{'status': 'Incoming friendship request'}],
            status=status.HTTP_200_OK
        )
    else:
        return Response(data=[{'status': 'None'}], status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    if User.objects.filter(username=username).exists():
        return Response(
            data=[{'message': 'User with this username already exists'}],
            status=status.HTTP_400_BAD_REQUEST
        )
    else:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(request.data, status=status.HTTP_200_OK)
