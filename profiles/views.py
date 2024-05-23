from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from rest_framework.exceptions import NotFound

class ProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer

class CurrentUserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        try:
            return UserProfile.objects.select_related('user').get(user=user)
        except UserProfile.DoesNotExist:
            raise NotFound("Profile does not exist for this user.")
