from rest_framework import serializers

from accounts.models import CustomUser
from adminfunc.models import ProbableFight
from profiles.serializers import VerifiedUserProfileSerializer


class ProbableFightSerializer(serializers.ModelSerializer):
    fighter1_username = serializers.CharField(write_only=True)
    fighter2_username = serializers.CharField(write_only=True)
    fighter1_details = VerifiedUserProfileSerializer(source='fighter1', read_only=True)
    fighter2_details = VerifiedUserProfileSerializer(source='fighter2', read_only=True)

    class Meta:
        model = ProbableFight
        fields = ['id', 'fighter1_username', 'fighter2_username', 'fighter1_details',
                  'fighter2_details', 'promotion_name', 'weight_category', 'created_at']
        read_only_fields = ['created_at']

    def validate(self, data):
        # Get fighters by username
        try:
            fighter1 = CustomUser.objects.get(username=data['fighter1_username'])
            fighter2 = CustomUser.objects.get(username=data['fighter2_username'])
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("One or both fighters not found")

        # Check if both fighters are verified
        if not (fighter1.is_verified and fighter2.is_verified):
            raise serializers.ValidationError("Both fighters must be verified")

        # Can't fight themselves
        if fighter1 == fighter2:
            raise serializers.ValidationError("A fighter cannot fight themselves")

        # Store the actual fighter objects
        data['fighter1'] = fighter1
        data['fighter2'] = fighter2

        # Remove the username fields as we don't need them anymore
        data.pop('fighter1_username')
        data.pop('fighter2_username')

        return data