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

class VerifiedUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='profile.full_name')
    date_of_birth = serializers.DateField(source='profile.birth_date')
    height = serializers.CharField(source='profile.height')
    weight = serializers.CharField(source='profile.weight')
    sport = serializers.CharField(source='profile.sport')

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'height', 'weight', 'sport', 'date_of_birth']

    def get_username(self, obj):
        return "@" + obj.username