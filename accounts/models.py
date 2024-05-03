from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from core import settings


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    height = models.CharField(max_length=50, blank=True)  # Height field added
    weight = models.CharField(max_length=50, blank=True)  # Weight field added
    martial_arts = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    experience = models.TextField(blank=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    description = models.TextField(blank=True)
    sports_title = models.BooleanField(default=False)
    title_photo = models.ImageField(upload_to='title_photos/', null=True, blank=True)
    fight_records = models.TextField(default=list)
    instagram_url = models.URLField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_promotion = models.BooleanField(default=False)


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