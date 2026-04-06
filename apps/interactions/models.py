from django.db import models
from django.conf import settings

# Create your models here.

class Comment(models.Model):
    resource = models.ForeignKey('resources.Resource', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resource = models.ForeignKey('resources.Resource', on_delete=models.CASCADE)

class Report(models.Model):
    resource = models.ForeignKey('resources.Resource', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reason = models.TextField()
