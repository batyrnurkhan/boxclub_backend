from rest_framework import serializers

from accounts.serializers import UserProfileSerializer
from .models import Post
from accounts.models import CustomUser, UserProfile


class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'is_verified', 'is_promotion', 'creator', 'profile']
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'birth_date', 'weight', 'height', 'sport', 'city', 'sport_time', 'profile_picture', 'description', 'rank', 'rank_file', 'video_links', 'instagram_link']