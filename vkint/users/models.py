from django.db import models
from django.contrib.auth import get_user_model


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
            models.UniqueConstraint(
                fields=['giver', 'reciever'],
                name='frequests_name'
            )
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
            models.UniqueConstraint(
                fields=['user_1', 'user_2'],
                name='friendship_name'
            )
        ]
