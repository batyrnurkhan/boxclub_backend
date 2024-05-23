from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from accounts.serializers import UserProfileSerializer

class ProfileListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer

class CurrentUserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """
        Return the profile of the currently logged-in user.
        """
        return self.request.user.profile
