from django.db import models
from meetings.models import Meeting
from django.contrib.auth import get_user_model

User = get_user_model()

class Key(models.Model):
    key = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_key',
    )
    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='Meeting'
    )
    link = models.TextField()
