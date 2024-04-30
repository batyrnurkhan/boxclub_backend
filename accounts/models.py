from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)

    full_name = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    height_weight = models.CharField(max_length=100, blank=True)
    martial_arts = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    experience = models.TextField(blank=True)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    description = models.TextField(blank=True)

    sports_title = models.CharField(max_length=100, blank=True)  # КМС или МС
    title_photo = models.ImageField(upload_to='title_photos/', null=True, blank=True)  # Фото сертификата
    fight_records = models.JSONField(default=list)  # Список URL для записей боев
    instagram_url = models.URLField(blank=True, null=True)

    is_verified = models.BooleanField(default=False)



    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'email']









