from django.contrib import admin
from .models import CustomUser, UserProfile, PromotionProfile, SubStatus, UserDocuments, WaitingVerifiedUsers, \
    Favourite, PlaceOfClasses
from django.contrib.auth.admin import UserAdmin  # Add this import


class CustomUserAdmin(UserAdmin):  # Change to inherit from UserAdmin instead of admin.ModelAdmin
    list_display = ('username', 'email', 'phone_number', 'is_verified', 'is_promotion', 'creator', 'is_staff')
    search_fields = ('username', 'email', 'phone_number', 'creator')
    list_filter = ('is_verified', 'is_promotion', 'is_staff', 'is_superuser')

    # The rest of your existing fieldsets
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'phone_number', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'creator')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_promotion')
        }),
    )

    # Add this for the password change form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'sport', 'status', 'is_verified', 'is_promotion')
    search_fields = ('user__username', 'full_name', 'city', 'sport')
    list_filter = ('status', 'is_verified', 'is_promotion')
    fieldsets = (
        (None, {
            'fields': ('user', 'username', 'full_name', 'birth_date', 'weight', 'height', 'sport', 'city', 'sport_time')
        }),
        ('Profile', {
            'fields': ('profile_picture', 'description', 'rank', 'rank_file', 'video_links', 'instagram_link')
        }),
        ('Status', {
            'fields': ('is_verified', 'is_promotion', 'status')
        }),
    )


class PromotionProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'creator', 'date_of_create')
    search_fields = ('user__username', 'city', 'creator')
    list_filter = ('date_of_create',)
    fieldsets = (
        (None, {
            'fields': ('user', 'city', 'creator', 'date_of_create', 'description')
        }),
        ('Links', {
            'fields': ('youtube_link', 'instagram_link', 'logo')
        }),
    )


class SubStatusAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'message', 'created_at')
    search_fields = ('user_profile__user__username', 'message')
    list_filter = ('created_at',)


class UserDocumentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'document1', 'document2', 'document3', 'document4')
    search_fields = ('user__username',)
    list_filter = ('user',)


class WaitingVerifiedUsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'birth_date', 'created_at')
    search_fields = ('user__username', 'full_name', 'city')
    list_filter = ('created_at',)


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'favourite_profile')
    search_fields = ('user__username', 'favourite_profile__user__username')
    list_filter = ('user', 'favourite_profile')


class PlaceOfClassesAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'city', 'sport', 'club_name', 'duration')
    search_fields = ('user_profile__user__username', 'city', 'sport', 'club_name')
    list_filter = ('sport', 'city')

    def get_username(self, obj):
        return obj.user_profile.user.username

    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user_profile__user__username'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user_profile":
            kwargs["queryset"] = UserProfile.objects.select_related('user')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def __str__(self):
        return f"{self.user_profile.user.username} - {self.city} - {self.club_name}"

admin.site.register(PlaceOfClasses, PlaceOfClassesAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PromotionProfile, PromotionProfileAdmin)
admin.site.register(SubStatus, SubStatusAdmin)
admin.site.register(UserDocuments, UserDocumentsAdmin)
admin.site.register(WaitingVerifiedUsers, WaitingVerifiedUsersAdmin)
admin.site.register(Favourite, FavouriteAdmin)

