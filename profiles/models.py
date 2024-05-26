# models.py

from django.db import models
from accounts.models import CustomUser
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)  # Make content optional
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Optional image field
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)  # Optional video field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)