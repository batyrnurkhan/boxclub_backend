from rest_framework import serializers
from accounts.models import CustomUser, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'full_name', 'birth_date', 'weight', 'height', 'sport', 'city',
            'sport_time', 'profile_picture', 'description', 'rank', 'rank_file',
            'video_links', 'instagram_link', 'is_verified', 'is_promotion', 'user'
        ]
        read_only_fields = ['user']
class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'is_verified', 'is_promotion', 'creator', 'profile']


class VerifiedUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='profile.full_name')
    date_of_birth = serializers.DateField(source='profile.birth_date')
    height = serializers.CharField(source='profile.height')
    weight = serializers.CharField(source='profile.weight')
    sport = serializers.CharField(source='profile.sport')
    is_verified = serializers.BooleanField(source='is_verified')
    is_promotion = serializers.BooleanField(source='is_promotion')

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'height', 'weight', 'sport', 'date_of_birth', 'is_verified', 'is_promotion']

    def get_username(self, obj):
        return f"@{obj.username}"
