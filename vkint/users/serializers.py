from rest_framework import serializers
from .models import User, Friendship, FRequest


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        fields = ['username', 'password']
        model = User


class FriendshipSerializer(serializers.ModelSerializer):
    user_1 = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username',
    )
    user_2 = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')

    class Meta:
        fields = ['user_1', 'user_2']
        model = Friendship


class FRequestSerializer(serializers.ModelSerializer):
    giver = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=User.objects.all(),
        slug_field='username',
    )
    reciever = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя отправить заявку в друзья себе'
            )
        return data

    class Meta:
        fields = ['giver', 'reciever']
        model = FRequest
