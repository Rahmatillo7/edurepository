from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "Categories"


class Subject(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='subjects/', blank=True)


class Resource(models.Model):
    LEVEL_CHOICES = [(i, f"{i}-sinf") for i in range(1, 12)]
    LANG_CHOICES = [('uz', 'O‘zbekcha'), ('ru', 'Ruscha'), ('en', 'Inglizcha')]

    title = models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    file = models.FileField(upload_to='resources/%Y/%m/')
    thumbnail = models.ImageField(upload_to='thumbnails/%Y/%m/', blank=True)

    description = models.TextField()
    class_level = models.IntegerField(choices=LEVEL_CHOICES, null=True, blank=True)
    language = models.CharField(max_length=2, choices=LANG_CHOICES, default='uz')

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
