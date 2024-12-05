# models.py

from django.db import models
from accounts.models import CustomUser, UserProfile
from django.conf import settings

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)  # Make content optional
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)  # Optional image field
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)  # Optional video field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class FightRecord(models.Model):
    STATUS_CHOICES = [
        ('WIN', 'Победа'),
        ('LOSE', 'Поражение'),
        ('DRAW', 'Ничья')
    ]

    user_profile = models.ForeignKey('accounts.UserProfile', on_delete=models.CASCADE, related_name='fight_records')
    status = models.CharField(max_length=4, choices=STATUS_CHOICES)
    opponent_name = models.CharField(max_length=255)
    promotion = models.CharField(max_length=255)
    fight_link = models.URLField(blank=True, null=True)
    weight_category = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
