from django.db import transaction
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import CustomUser, UserProfile

@receiver(post_save, sender=CustomUser)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, username=instance.username)
    else:
        user_profile, created = UserProfile.objects.get_or_create(user=instance)
        update_fields = []
        for field in ['is_verified', 'is_promotion', 'username']:
            user_value = getattr(instance, field)
            profile_value = getattr(user_profile, field)
            if user_value != profile_value:
                setattr(user_profile, field, user_value)
                update_fields.append(field)
        if update_fields:
            user_profile.save(update_fields=update_fields)

@receiver(post_save, sender=UserProfile)
def update_custom_user(sender, instance, created, **kwargs):
    if not created:
        custom_user = instance.user
        update_fields = []
        for field in ['is_verified', 'is_promotion', 'username']:
            profile_value = getattr(instance, field)
            user_value = getattr(custom_user, field)
            if user_value != profile_value:
                setattr(custom_user, field, profile_value)
                update_fields.append(field)
        if update_fields:
            custom_user.save(update_fields=update_fields)

@receiver(pre_delete, sender=CustomUser)
def delete_user_profile(sender, instance, **kwargs):
    # Assuming UserProfile should be deleted when CustomUser is deleted
    if hasattr(instance, 'profile'):
        instance.profile.delete()
