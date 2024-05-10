from rest_framework import serializers

from accounts.models import CustomUser
from .models import News

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

