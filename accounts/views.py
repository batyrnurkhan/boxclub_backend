from .serializers import RegisterSerializer, UserDetailsSerializer, UserSportsDetailsSerializer, LoginSerializer
from .serializers import PromotionDescriptionSerializer, PromotionRegisterSerializer, PromotionDetailSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout

from rest_framework import views, status, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


class IsPromotionUser(permissions.BasePermission):
    """
    Allows access only to users who have is_promotion set to True.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has is_promotion set to True
        return request.user and request.user.is_authenticated and request.user.is_promotion


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save()  # This saves the user instance
        login(self.request, user)  # Log the user in immediately after registration
        return user

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Assuming the registration was successful and the user is now logged in,
        # modify the response to indicate that the user was also logged in.
        if response.status_code == 201:
            response.data['message'] = 'User registered and logged in successfully.'
        return response


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
        return self.request.user


class PromotionRegisterView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PromotionRegisterSerializer
    permission_classes = [permissions.IsAuthenticated, IsPromotionUser]  # Add custom permission here

    def get_object(self):
        # The user is implicitly allowed by the permissions to update their own profile
        return self.request.user


class PromotionDescriptionView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PromotionDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsPromotionUser]  # Add custom permission here

    def get_object(self):
        # The user is implicitly allowed by the permissions to update their own profile
        return self.request.user


class PromotionDetailView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PromotionDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsPromotionUser]  # Add custom permission here

    def get_object(self):
        # The user is implicitly allowed by the permissions to update their own profile
        return self.request.user


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "User logged in successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]  # Ensures only logged-in users can log out

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_204_NO_CONTENT)


