from rest_framework import serializers

from accounts.serializers import UserProfileSerializer
from .models import Post
from accounts.models import CustomUser, UserProfile


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'video', 'created_at', 'updated_at']

    def validate(self, data):
        # Check if neither image nor video is provided
        if not data.get('image') and not data.get('video'):
            raise serializers.ValidationError("An image or video is required to create a post.")
        return data


class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['full_name', 'birth_date', 'weight', 'height', 'sport', 'city', 'sport_time', 'profile_picture',
                  'description', 'rank', 'rank_file', 'video_links', 'instagram_link', 'posts']


class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)
    is_profile_owner = serializers.SerializerMethodField()
    edit_profile_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'is_verified', 'is_promotion', 'creator', 'profile', 'posts', 'is_profile_owner', 'edit_profile_url']

    def get_is_profile_owner(self, obj):
        # Check if the profile belongs to the current user
        request = self.context.get('request')
        if request and request.user.is_authenticated and obj == request.user:
            return True
        return False

    def get_edit_profile_url(self, obj):
        # Provide the URL to edit the profile only if the current user is the profile owner
        request = self.context.get('request')
        if request and request.user.is_authenticated and obj == request.user:
            return request.build_absolute_uri('/profiles/edit/')
        return None

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


