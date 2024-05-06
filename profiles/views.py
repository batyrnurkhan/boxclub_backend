from rest_framework import viewsets, permissions
from .models import Post
from accounts.models import CustomUser
from .serializers import UserProfileSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access user profiles
