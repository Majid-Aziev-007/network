from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Subscribe(models.Model):
    """
        Модель подписки
        user - Юзер
        date_start - День старта подписки
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    date_start = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_username()
