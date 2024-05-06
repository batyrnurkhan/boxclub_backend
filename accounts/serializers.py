import random
import string
import uuid

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from accounts.models import UserProfile, PromotionProfile, CustomUser

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
        model = User
        fields = [
            'full_name', 'birth_date', 'height_weight', 'martial_arts',
            'city', 'experience', 'photo', 'description'
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserSportsDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['sports_title', 'title_photo', 'fight_records', 'instagram_url']

    def update(self, instance, validated_data):
        instance.sports_title = validated_data.get('sports_title', instance.sports_title)
        instance.title_photo = validated_data.get('title_photo', instance.title_photo)
        instance.fight_records = validated_data.get('fight_records', instance.fight_records)
        instance.instagram_url = validated_data.get('instagram_url', instance.instagram_url)
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
        model = User
        fields = ['description']

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class PromotionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['instagram_url', 'fight_records', 'photo']

    def update(self, instance, validated_data):
        instance.instagram_url = validated_data.get('instagram_url', instance.instagram_url)
        instance.fight_records = validated_data.get('fight_records', instance.fight_records)
        instance.photo = validated_data.get('photo', instance.photo)
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

class PromotionProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionProfile
        fields = '__all__'