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
    STATUS_CHOICES = [
        ('Free', 'Free'),
        ('Ready to fight', 'Ready to fight'),
        ('Injury', 'Injury'),
        ('I will be ready in 30 days', 'I will be ready in 30 days'),
        ('I will be ready in 60 days', 'I will be ready in 60 days'),
        ('I will be ready in 90 days', 'I will be ready in 90 days'),
        ('I have a contract', 'I have a contract'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    username = models.CharField(max_length=150, blank=True)  # New field for storing username
    full_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)  # Allow null
    weight = models.IntegerField(null=True, blank=True)  # Changed to IntegerField
    height = models.CharField(max_length=50, null=True, blank=True)
    sport = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    sport_time = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles_pictures/', null=True, blank=True)
    description = models.TextField(blank=True)
    rank = models.BooleanField(default=False)
    rank_file = models.FileField(upload_to='rank_files/', null=True, blank=True)
    video_links = models.JSONField(default=list, null=True, )
    instagram_link = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_promotion = models.BooleanField(default=False)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Free')


class UserDocuments(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    document1 = models.FileField(upload_to='user_documents/')
    document2 = models.FileField(upload_to='user_documents/')
    document3 = models.FileField(upload_to='user_documents/')
    document4 = models.FileField(upload_to='user_documents/')

    def __str__(self):
        return f"Documents for {self.user.username}"


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
        return now().year - self.birth_date.year - (
                    (now().month, now().day) < (self.birth_date.month, self.birth_date.day))


class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites')
    favourite_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='favourited_by')

    class Meta:
        unique_together = ('user', 'favourite_profile')

    def __str__(self):
        return f"{self.user.username} likes {self.favourite_profile.user.username}"


class SubStatus(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='substatuses')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SubStatus for {self.user_profile.user.username}: {self.message}"