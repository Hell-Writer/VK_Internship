from django.shortcuts import get_object_or_404
from .models import Follow, User, Friendship, FRequest
from rest_framework import filters, mixins, viewsets, status
from .serializers import FollowSerializer, UserSerializer, FriendshipSerializer, FRequestSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.db.models import Q

@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def follow(request):
    if request.method == "GET" and request.data.get("type") == 'followers':
        followers = Follow.objects.filter(following=request.user)
        serializer = FollowSerializer(followers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == "GET" and request.data.get("type") == 'following':
        followers = Follow.objects.filter(follower=request.user)
        serializer = FollowSerializer(followers, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == "DELETE":
        user_2 = get_object_or_404(User, username=request.data.get('person'))
        if Follow.objects.filter(following=user_2, follower=request.user).exists():
            Follow.objects.get(following=user_2, follower=request.user).delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if FRequest.objects.filter(reciever=user_2, giver=request.user).exists():
            FRequest.objects.get(reciever=user_2, giver=request.user).delete()
        if Friendship.objects.filter(user_1=user_2, user_2=request.user).exists():
            Friendship.objects.get(user_1=user_2, user_2=request.user).delete()
        if Friendship.objects.filter(user_2=user_2, user_1=request.user).exists():
            Friendship.objects.get(user_2=user_2, user_1=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == "POST":
        user = request.user
        following = get_object_or_404(User, username=request.data.get("person"))
        Follow.objects.create(follower=user, following=following)
        FRequest.objects.create(giver=user, reciever=following)
        if FRequest.objects.filter(reciever=user, giver=following).exists():
            Friendship.objects.create(user_1=user, user_2=following)
            Friendship.objects.create(user_2=user, user_1=following)
            FRequest.objects.filter(reciever=user, giver=following).delete()
            FRequest.objects.filter(giver=user, reciever=following).delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET", "DELETE"])
@permission_classes([IsAuthenticated])
def friends(request):
    user = request.user
    if request.method == "GET":
        friends = Friendship.objects.filter(user_1=user)
        serializer = FriendshipSerializer(friends, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == "DELETE":
        friend = get_object_or_404(User, username=request.data.get('person'))
        if Friendship.objects.filter(user_1=user, user_2=friend).exists():
            Friendship.objects.filter(user_1=user, user_2=friend).delete()
            Friendship.objects.filter(user_2=user, user_1=friend).delete()
            Follow.objects.filter(following=user, follower=friend).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
def friend_request(request):
    user = request.user
    if request.method == "GET" and request.data.get("type") == 'incoming':
        frequests = FRequest.objects.filter(reciever=user)
        serializer = FRequestSerializer(frequests, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == "GET" and request.data.get("type") == 'outcoming':
        frequests = FRequest.objects.filter(giver=user)
        serializer = FRequestSerializer(frequests, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    if request.method == "POST":
        FRgiver = get_object_or_404(User, username=request.data.get('person'))
        if request.data.get("type") == 'accept':
            frequest = get_object_or_404(FRequest, reciever=user, giver=FRgiver)
            frequest.delete()
            Follow.objects.create(follower=user, following=FRgiver)
            Friendship.objects.create(user_1=user, user_2=FRgiver)
            Friendship.objects.create(user_2=user, user_1=FRgiver)
        elif request.data.get("type") == 'decline':
            frequest = get_object_or_404(FRequest, reciever=user, giver=FRgiver)
            frequest.delete()
        elif request.data.get("type") == 'send':
            FRequest.objects.create(giver=user, reciever=FRgiver)
            if not Follow.objects.filter(follower=user, following=FRgiver).exists():
                Follow.objects.create(follower=user, following=FRgiver)
            if Follow.objects.filter(following=user, follower=FRgiver).exists():
                FRequest.objects.filter(giver=user, reciever=FRgiver).delete()
                Friendship.objects.create(user_1=user, user_2=FRgiver)
                Friendship.objects.create(user_2=user, user_1=FRgiver)
            if FRequest.objects.filter(reciever=user, giver=FRgiver).exists():
                FRequest.objects.filter(reciever=user, giver=FRgiver).delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
    if request.method == "DELETE":
        FRreciever = get_object_or_404(User, username=request.data.get('person'))
        if FRequest.objects.filter(giver=user, reciever=FRreciever).exists():
            FRequest.objects.filter(giver=user, reciever=FRreciever).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def friendship_status(request):
    user = request.user
    person = get_object_or_404(User, username=request.data.get('person'))
    if Friendship.objects.filter(user_1=user, user_2=person).exists():
        return Response(data=[{'status': 'Friend'}], status=status.HTTP_200_OK)
    elif FRequest.objects.filter(giver=user, reciever=person).exists():
        return Response(data=[{'status': 'Outcoming friendship request'}], status=status.HTTP_200_OK)
    elif FRequest.objects.filter(reciever=user, giver=person).exists():
        return Response(data=[{'status': 'Incoming friendship request'}], status=status.HTTP_200_OK)
    else:
        return Response(data=[{'status': 'None'}], status=status.HTTP_200_OK)


class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    @action(methods=['get'], detail=False,
            serializer_class=UserSerializer,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if self.request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    if User.objects.filter(username=username).exists() or username=='me':
        return Response(data=[{'message': 'User with this username already exists'}], status=status.HTTP_200_OK)
    else:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = get_object_or_404(
            User,
            username=serializer.validated_data["username"]
        )
        return Response(request.data, status=status.HTTP_200_OK)
