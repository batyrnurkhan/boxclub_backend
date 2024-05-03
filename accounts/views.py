from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .models import WaitingVerifiedUsers
from .serializers import RegisterSerializer, UserDetailsSerializer, UserSportsDetailsSerializer, LoginSerializer, \
    SuperuserPromotionRegisterSerializer, UserVerificationSerializer, PaymentSerializer
from .serializers import PromotionDescriptionSerializer, PromotionRegisterSerializer, PromotionDetailSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework import views, status, permissions, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "User logged in successfully.",
                "token": token.key
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]  # Ensures only logged-in users can log out

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_204_NO_CONTENT)


class PromotionUserCreateView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]  # Ensure using Token Authentication only

    def post(self, request, *args, **kwargs):
        request.data['is_promotion'] = True  # Explicitly setting is_promotion here
        serializer = SuperuserPromotionRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "Promotion user registered successfully.",
                "user_id": user.id,
                "username": user.username,
                "full_name": user.full_name,
                "password": user.plain_password  # Assuming plain_password is managed as discussed
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetUserVerificationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if user is already verified
        if user.is_verified:
            return Response({"message": "Already has verification."})

        # Set the user as verified
        user.is_verified = True
        user.save()
        return Response({"message": "Verification set."})

class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        # Check if the user is already verified
        if user.is_verified:
            return Response({"message": "You are already verified, you can't verify twice."}, status=400)

        # Check if the user is already in the waiting list
        if WaitingVerifiedUsers.objects.filter(user=user).exists():
            return Response({"message": "You have already requested to be verified, please wait."}, status=400)

        # If not verified and not in the waiting list, add them to the waiting list
        WaitingVerifiedUsers.objects.create(
            user=user,
            full_name=user.full_name,
            city=user.city,
            height=user.height,
            weight=user.weight,
            birth_date=user.birth_date
        )
        return Response({"message": "Payment submitted. Waiting for verification."}, status=201)


class WaitingVerifiedUsersListView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        # Fetching all records
        waiting_users = WaitingVerifiedUsers.objects.all().values(
            'full_name', 'city', 'height', 'weight', 'birth_date', 'created_at'
        )
        # Returning the list of waiting users and their data
        return Response({"waiting_verified_users": list(waiting_users)})