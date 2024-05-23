from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserProfile

@receiver(post_save, sender=CustomUser)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a new UserProfile when a new CustomUser is created
        UserProfile.objects.create(user=instance, username=instance.username)
    else:
        try:
            # Update the UserProfile if it exists
            user_profile = UserProfile.objects.get(user=instance)
            update_fields = []
            # Synchronize is_verified and is_promotion
            if user_profile.is_verified != instance.is_verified:
                user_profile.is_verified = instance.is_verified
                update_fields.append('is_verified')
            if user_profile.is_promotion != instance.is_promotion:
                user_profile.is_promotion = instance.is_promotion
                update_fields.append('is_promotion')
            # Synchronize username separately
            if user_profile.username != instance.username:
                user_profile.username = instance.username
                update_fields.append('username')
            if update_fields:
                user_profile.save(update_fields=update_fields)
        except UserProfile.DoesNotExist:
            # Create a UserProfile if it does not exist (optional handling)
            UserProfile.objects.create(
                user=instance,
                is_verified=instance.is_verified,
                is_promotion=instance.is_promotion,
                username=instance.username
            )

@receiver(post_save, sender=UserProfile)
def update_custom_user(sender, instance, created, **kwargs):
    if not created:
        custom_user = instance.user
        update_fields = []
        # Synchronize is_verified and is_promotion
        if custom_user.is_verified != instance.is_verified:
            custom_user.is_verified = instance.is_verified
            update_fields.append('is_verified')
        if custom_user.is_promotion != instance.is_promotion:
            custom_user.is_promotion = instance.is_promotion
            update_fields.append('is_promotion')
        # Synchronize username separately
        if custom_user.username != instance.username:
            custom_user.username = instance.username
            update_fields.append('username')
        if update_fields:
            custom_user.save(update_fields=update_fields)
