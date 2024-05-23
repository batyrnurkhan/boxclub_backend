from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from core import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_promotion = models.BooleanField(default=False)
    creator = models.CharField(max_length=100, null=True, blank=True)  # Optional creator field


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)  # Allow null
    weight = models.IntegerField(null=True, blank=True)  # Changed to IntegerField
    height = models.CharField(max_length=50, null=True, blank=True)
    sport = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    sport_time = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    description = models.TextField(blank=True)
    rank = models.BooleanField(default=False)
    rank_file = models.FileField(upload_to='rank_files/', null=True, blank=True)
    video_links = models.JSONField(default=list, null=True,)
    instagram_link = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)  # Added directly to UserProfile
    is_promotion = models.BooleanField(default=False)  # Added directly to UserProfile

class PromotionProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='promotion_profile')
    city = models.CharField(max_length=100)
    creator = models.CharField(max_length=100)
    date_of_create = models.DateField()
    description = models.TextField(blank=True)
    youtube_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)

class WaitingVerifiedUsers(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    height = models.CharField(max_length=50, blank=True)  # Separate height field
    weight = models.CharField(max_length=50, blank=True)  # Separate weight field
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def age(self):
        return now().year - self.birth_date.year - ((now().month, now().day) < (self.birth_date.month, self.birth_date.day))