from django.contrib import admin
from .models import CustomUser, UserProfile, WaitingVerifiedUsers


admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(WaitingVerifiedUsers)
