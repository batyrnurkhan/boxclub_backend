import random
import string
import uuid

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import UserProfile, PromotionProfile, CustomUser, WaitingVerifiedUsers, UserDocuments, Favourite, \
    SubStatus

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'full_name', 'birth_date', 'weight', 'height', 'sport',
            'city', 'sport_time', 'profile_picture', 'description'
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


from rest_framework import serializers
from .models import UserProfile


class UserSportsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['rank_file', 'video_links', 'instagram_link']

    def update(self, instance, validated_data):
        instance.rank_file = validated_data.get('rank_file', instance.rank_file)
        instance.video_links = validated_data.get('video_links', instance.video_links)
        instance.instagram_link = validated_data.get('instagram_link', instance.instagram_link)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is not None:
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class PromotionRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['city', 'full_name', 'birth_date']

    def update(self, instance, validated_data):
        instance.city = validated_data.get('city', instance.city)
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()
        return instance


class PromotionDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionProfile
        fields = ['description']

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class PromotionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionProfile
        fields = ['instagram_link', 'youtube_link', 'logo']

    def update(self, instance, validated_data):
        instance.instagram_link = validated_data.get('instagram_link', instance.instagram_link)
        instance.youtube_link = validated_data.get('youtube_link', instance.youtube_link)
        instance.logo = validated_data.get('logo', instance.logo)
        instance.save()
        return instance


class SuperuserPromotionRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'creator', 'is_promotion')

    def create(self, validated_data):
        # Generate a random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=11))
        # Hash the password
        validated_data['password'] = make_password(password)
        validated_data['is_promotion'] = True
        # Create the user
        user = CustomUser.objects.create(**validated_data)
        user.save()
        # Attach the plain password temporarily to the instance
        user.plain_password = password
        return user


class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_verified']

    def update(self, instance, validated_data):
        if instance.is_verified:
            raise serializers.ValidationError("Already has verification.")
        instance.is_verified = True
        instance.save()
        return instance


class PaymentSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, min_length=16)
    expire_date = serializers.DateField(input_formats=['%m/%y'])  # Format: "MM/YY"
    cvv = serializers.CharField(max_length=4, min_length=3)  # 3 or 4 digits

    def validate_card_number(self, value):
        # Add card number validation logic here (e.g., Luhn algorithm)
        return value

    def validate_expire_date(self, value):
        # Add expiration date validation logic here
        return value

    def validate_cvv(self, value):
        # Add CVV validation logic here
        return value


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        ref_name = "AccountsUserProfile"


class PromotionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionProfile
        fields = ['city', 'description', 'youtube_link', 'instagram_link', 'logo', 'date_of_create', 'creator']

    def update(self, instance, validated_data):
        instance.date_of_create = validated_data.get('date_of_create', instance.date_of_create)
        return super().update(instance, validated_data)


class SimpleUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']


class VerifiedUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='profile.full_name')
    date_of_birth = serializers.DateField(source='profile.birth_date')
    height = serializers.CharField(source='profile.height')
    weight = serializers.CharField(source='profile.weight')
    sport = serializers.CharField(source='profile.sport')
    city = serializers.CharField(source='profile.city')
    status = serializers.CharField(source='profile.status')  # Added status field
    profile = SimpleUserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'full_name', 'height', 'weight', 'sport',
            'date_of_birth', 'city', 'status', 'profile'
        ]

    def get_username(self, obj):
        return "@" + obj.username


class RegistrationStatsSerializer(serializers.Serializer):
    users_registered_today = serializers.IntegerField()
    users_registered_past_month = serializers.IntegerField()


class WaitingVerifiedUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = WaitingVerifiedUsers
        fields = ['full_name', 'city', 'height', 'weight', 'birth_date', 'created_at', 'profile']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_profile = UserProfile.objects.filter(user=instance.user).first()
        if user_profile:
            profile_serializer = UserProfileSerializer(user_profile)
            representation['profile'] = profile_serializer.data
        return representation


class UserDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDocuments
        fields = ['document1', 'document2', 'document3', 'document4']


class UserProfileStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['status']


class FavouriteSerializer(serializers.ModelSerializer):
    favourite_profile = UserProfileSerializer(read_only=True)  # Nested serializer

    class Meta:
        model = Favourite
        fields = ['user', 'favourite_profile']
        read_only_fields = ['user']


class SubStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubStatus
        fields = ['id', 'message', 'created_at']

