from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_teacher = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.username