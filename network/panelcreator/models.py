from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Creator(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='creator',
    )

    percentage_of_earnings = models.IntegerField()
    paid = models.IntegerField()
