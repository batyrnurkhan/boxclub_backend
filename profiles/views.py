
from rest_framework import viewsets
from .models import Post
from accounts.models import CustomUser

from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer