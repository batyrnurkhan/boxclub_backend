from rest_framework import serializers
from .models import Post
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'instagram_url', 'username', 'birth_date', 'height', 'weight', 'martial_arts', 'city']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)  # Simplified the naming to 'posts' to match the model relationship

    class Meta:
        model = CustomUser
        fields = ['full_name', 'instagram_url', 'username', 'birth_date', 'height', 'weight', 'martial_arts', 'city', 'posts']
