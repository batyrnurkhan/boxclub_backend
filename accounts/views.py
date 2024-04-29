from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .serializers import RegisterSerializer, UserDetailsSerializer, UserSportsDetailsSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()
        # Automatically log the user in or send a verification link here
        redirect_url = reverse('user-details-update', kwargs={'pk': user.pk})
        return Response({'redirect_url': redirect_url}, status=status.HTTP_302_FOUND)

    def get_object(self):
        return self.request.user

class UserDetailsUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserSportsDetailsUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSportsDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure that a user can only update their own sports details
        return self.request.user
