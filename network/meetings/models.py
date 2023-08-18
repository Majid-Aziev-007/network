from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Topic(models.Model):
    """Тематика Нетворкинга"""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Meeting(models.Model):
    """Нетворк"""

    CHOICES = (
        ('OFF', 'Offline'),
        ('ON', 'Online'),
    )

    type = models.CharField(
        max_length=300,
        choices=CHOICES,
        blank=True,
        null=True
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    meeting_date = models.DateTimeField(
        blank=True,
        null=True,
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meetings'
    )
    topic = models.ForeignKey(
        Topic,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='topic'
    )

    def __str__(self):
        return self.title


class Presence(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='participant',
        null=True
    )

    meeting = models.ForeignKey(
        Meeting,
        on_delete=models.CASCADE,
        related_name='meeting'
    )
