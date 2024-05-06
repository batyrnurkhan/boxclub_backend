from django.shortcuts import get_list_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from .models import WaitingVerifiedUsers, UserProfile, PromotionProfile, CustomUser
from .serializers import RegisterSerializer, UserDetailsSerializer, UserSportsDetailsSerializer, LoginSerializer, \
    SuperuserPromotionRegisterSerializer, UserVerificationSerializer, PaymentSerializer, PromotionProfileSerializer, \
    UserProfileSerializer, VerifiedUserProfileSerializer
from .serializers import PromotionDescriptionSerializer, PromotionRegisterSerializer, PromotionDetailSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework import views, status, permissions, generics, serializers
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
        if not user.is_promotion:
            UserProfile.objects.create(user=user)  # Automatically create a user profile for non-promotional users
        return user

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Assuming the registration was successful and the user is now logged in,
        # modify the response to indicate that the user was also logged in.
        if response.status_code == 201:
            response.data['message'] = 'User registered and logged in successfully.'
        return response

class UserProfileCreateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

class PromotionProfileCreateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PromotionProfile.objects.all()
    serializer_class = PromotionProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsPromotionUser]

    def get_object(self):
        return self.request.user.promotion_profile
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


class PromotionRegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SuperuserPromotionRegisterSerializer
    permission_classes = [permissions.IsAdminUser]  # Assuming only admins can create promotional users

    def perform_create(self, serializer):
        # This method will handle the creation of the user and profile
        user = serializer.save(is_promotion=True)  # Save user with is_promotion set to True

        # Assuming PromotionProfile data is also sent in the request, let's create the profile
        profile_data = {
            'user': user,
            'city': self.request.data.get('city', ''),
            'creator': self.request.data.get('creator', ''),
            'date_of_create': self.request.data.get('date_of_create', ''),
            'description': self.request.data.get('description', ''),
            'youtube_link': self.request.data.get('youtube_link', ''),
            'instagram_link': self.request.data.get('instagram_link', ''),
            'logo': self.request.data.get('logo', ''),
        }
        profile_serializer = PromotionProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            user.delete()  # Rollback the user creation if the profile is invalid
            raise serializers.ValidationError(profile_serializer.errors)

    def create(self, request, *args, **kwargs):
        # Override the create method to handle creation of both user and profile
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            response.data['message'] = 'Promotion user and profile created successfully.'
        return response

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


class PromotionUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SuperuserPromotionRegisterSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save()
        # Manually add password to the response
        self.password = user.plain_password  # Store password to add to the response after save

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Add the password to the response data
            response.data['password'] = self.password
        return response

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


class VerifiedUsersListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_superuser or request.user.is_promotion:
            search_query = request.query_params.get('search', '')
            users = get_list_or_404(CustomUser, is_verified=True, username__icontains=search_query)
            serializer = VerifiedUserProfileSerializer(users, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "You do not have permission to view this list."}, status=403)


class RejectVerificationView(APIView):
    def post(self, request, user_id, *args, **kwargs):
        try:
            # Попытка найти пользователя в ожидающих верификации
            waiting_user = WaitingVerifiedUsers.objects.get(user_id=user_id)
            # Если пользователь найден, удаляем его из базы данных
            waiting_user.delete()
            return Response({"message": "Вам отказано в верификации."}, status=status.HTTP_200_OK)
        except WaitingVerifiedUsers.DoesNotExist:
            # Если пользователя с заданным идентификатором нет в ожидающих верификации,
            # возвращаем сообщение об ошибке
            return Response({"message": "Пользователь не найден в ожидающих верификации."}, status=status.HTTP_404_NOT_FOUND)