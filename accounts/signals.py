from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile

@receiver(post_save, sender=CustomUser)
def update_user_profile(sender, instance, created, **kwargs):
    if not created:
        user_profile = UserProfile.objects.get(user=instance)
        if (user_profile.is_verified != instance.is_verified or user_profile.is_promotion != instance.is_promotion):
            user_profile.is_verified = instance.is_verified
            user_profile.is_promotion = instance.is_promotion
            user_profile.save()

@receiver(post_save, sender=UserProfile)
def update_custom_user(sender, instance, created, **kwargs):
    if not created:
        custom_user = CustomUser.objects.get(id=instance.user.id)
        if (custom_user.is_verified != instance.is_verified or custom_user.is_promotion != instance.is_promotion):
            custom_user.is_verified = instance.is_verified
            custom_user.is_promotion = instance.is_promotion
            custom_user.save()
