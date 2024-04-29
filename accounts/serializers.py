from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

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
