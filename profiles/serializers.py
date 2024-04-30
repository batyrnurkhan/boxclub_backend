from rest_framework import serializers
from .models import Post
from accounts.models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'instagram_url', 'username', 'birth_date', 'height_weight', 'martial_arts', 'city']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']

class UserProfileSerializer(serializers.ModelSerializer):
    posts2 = PostSerializer(many=True, source='posts')  # Use the related_name from the ForeignKey in Post model

    class Meta:
        model = CustomUser
        fields = ['full_name', 'instagram_url', 'username', 'birth_date', 'height_weight', 'martial_arts', 'city', 'posts2']

# Use this serializer in your views to get user details along with their posts
