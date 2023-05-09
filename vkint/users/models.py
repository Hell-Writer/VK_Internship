from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator


User = get_user_model()


class FRequest(models.Model):
    giver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='giver'
    )
    reciever = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reciever'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['giver', 'reciever'], name='frequests_name')
        ]


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='follow_name')
        ]


class Friendship(models.Model):
    user_1 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_1'
    )
    user_2 = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_2'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_1', 'user_2'], name='friendship_name')
        ]
