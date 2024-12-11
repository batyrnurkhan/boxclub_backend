from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.utils import timezone

from .models import WaitingVerifiedUsers, UserProfile, PromotionProfile, CustomUser, UserDocuments, Favourite, \
    SubStatus, UserDocuments, Achievement, PlaceOfClasses
from .serializers import RegisterSerializer, UserDetailsSerializer, UserSportsDetailsSerializer, LoginSerializer, \
    SuperuserPromotionRegisterSerializer, UserVerificationSerializer, PaymentSerializer, PromotionProfileSerializer, \
    UserProfileSerializer, VerifiedUserProfileSerializer, WaitingVerifiedUserSerializer, UserDocumentsSerializer, \
    UserProfileStatusSerializer, FavouriteSerializer, SubStatusSerializer, UserDocumentsSerializer, \
    AchievementSerializer, PlaceOfClassesSerializer, ChangePasswordSerializer
from .serializers import PromotionDescriptionSerializer, PromotionRegisterSerializer, PromotionDetailSerializer, \
    RegistrationStatsSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from rest_framework.authtoken.models import Token
from rest_framework import views, status, permissions, generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

User = get_user_model()

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="Detailed documentation of all API endpoints",
    ),
    public=True,
    permission_classes=[AllowAny],
    authentication_classes=[TokenAuthentication]
)


class IsPromotionUser(permissions.BasePermission):
    """
    Allows access only to users who have is_promotion set to True.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has is_promotion set to True
        return request.user and request.user.is_authenticated and request.user.is_promotion


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Log the user in
        login(request, user)

        # Create response data
        response_data = {
            'message': 'User registered and logged in successfully.',
            'username': user.username,
            'phone_number': user.phone_number,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


# class UserProfileCreateUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#     @swagger_auto_schema(
#         operation_description="Retrieve or update the authenticated user's profile.",
#         responses={
#             200: UserProfileSerializer,
#             404: 'Profile not found'
#         }
#     )
#     def get_object(self):
#         return self.request.user.profile
#
# class PromotionProfileCreateUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = PromotionProfile.objects.all()
#     serializer_class = PromotionProfileSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPromotionUser]
#
#     @swagger_auto_schema(
#         operation_description="Retrieve or update the promotion profile for the authenticated user.",
#         responses={
#             200: PromotionProfileSerializer,
#             404: 'Promotion profile not found'
#         }
#     )
#     def get_object(self):
#         return self.request.user.promotion_profile
class UserDetailsUpdateView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class UserSportsDetailsUpdateView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()  # Change this to UserProfile
    serializer_class = UserSportsDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the UserProfile object associated with the request user
        return UserProfile.objects.get(user=self.request.user)


class PromotionRegisterView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = PromotionProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'city': 'Default City', 'date_of_create': timezone.now()}  # Provide default date
        )
        return profile

    def get_serializer_class(self):
        return PromotionProfileSerializer


class PromotionDescriptionView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = PromotionDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated, IsPromotionUser]  # Add custom permission here

    def get_object(self):
        # The user is implicitly allowed by the permissions to update their own profile
        return self.request.user


class PromotionDetailView(generics.UpdateAPIView):
    queryset = PromotionProfile.objects.all()
    serializer_class = PromotionDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsPromotionUser]

    def get_object(self):
        # Fetch the PromotionProfile for the authenticated user
        return get_object_or_404(PromotionProfile, user=self.request.user)


class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login a user by obtaining a token.",
        request_body=LoginSerializer,
        responses={200: openapi.Response('Successful Login', LoginSerializer)},
    )
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

    @swagger_auto_schema(
        operation_description="Log out the current user.",
        responses={204: 'Logged out successfully'}
    )
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_204_NO_CONTENT)


class PromotionUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SuperuserPromotionRegisterSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save()
        # Explicitly create a PromotionProfile
        PromotionProfile.objects.get_or_create(
            user=user,
            defaults={'city': 'Default City', 'date_of_create': timezone.now()}
        )
        # Manually add password to the response
        self.password = user.plain_password

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == status.HTTP_201_CREATED:
            # Add the password to the response data
            response.data['password'] = self.password
        return response


class SetUserVerificationView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, username, *args, **kwargs):
        # Fetch the user by username
        user = get_object_or_404(CustomUser, username=username)

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

        if user.is_verified:
            return Response({"message": "You are already verified, you can't verify twice."}, status=400)

        if WaitingVerifiedUsers.objects.filter(user=user).exists():
            return Response({"message": "You have already requested to be verified, please wait."}, status=400)

        user_profile = user.profile

        WaitingVerifiedUsers.objects.create(
            user=user,
            full_name=user_profile.full_name,
            city=user_profile.city,
            height=user_profile.height,
            weight=user_profile.weight,
            birth_date=user_profile.birth_date
        )
        return Response({"message": "Payment submitted. Waiting for verification."}, status=201)


class WaitingVerifiedUsersListView(generics.ListAPIView):
    serializer_class = WaitingVerifiedUserSerializer
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = WaitingVerifiedUsers.objects.filter(user__is_verified=False).select_related('user').prefetch_related(
            'user__profile')
        full_name = self.request.query_params.get('full_name')
        city = self.request.query_params.get('city')
        height = self.request.query_params.get('height')
        weight = self.request.query_params.get('weight')
        sport = self.request.query_params.get('sport')

        if full_name:
            queryset = queryset.filter(user__profile__full_name__icontains=full_name)
        if city:
            queryset = queryset.filter(user__profile__city__icontains=city)
        if height:
            queryset = queryset.filter(user__profile__height__icontains=height)
        if weight:
            queryset = queryset.filter(user__profile__weight=weight)
        if sport:
            queryset = queryset.filter(user__profile__sport__icontains=sport)
        return queryset


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
    def post(self, request, username, *args, **kwargs):
        # Attempt to find the waiting verification entry using the username
        user = get_object_or_404(CustomUser, username=username)
        try:
            waiting_user = WaitingVerifiedUsers.objects.get(user=user)
            # If found, delete the waiting verification entry
            waiting_user.delete()
            return Response({"message": "Verification request rejected."}, status=200)
        except WaitingVerifiedUsers.DoesNotExist:
            # If no waiting verification entry found, return error
            return Response({"message": "User not found in waiting verification."}, status=404)


class UserSearchListView(generics.ListAPIView):
    serializer_class = VerifiedUserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = CustomUser.objects.filter(is_verified=True)
        queries = []

        weight_min = self.request.query_params.get('weight_min')
        weight_max = self.request.query_params.get('weight_max')
        full_name = self.request.query_params.get('full_name')
        height = self.request.query_params.get('height')
        sport = self.request.query_params.get('sport')
        city = self.request.query_params.get('city')
        sport_time = self.request.query_params.get('sport_time')
        rank = self.request.query_params.get('rank')

        if weight_min and weight_max:
            weight_min = int(weight_min)
            weight_max = int(weight_max)
            queries.append(Q(profile__weight__gte=weight_min) & Q(profile__weight__lte=weight_max))
        if full_name:
            queries.append(Q(profile__full_name__icontains=full_name))
        if height:
            queries.append(Q(profile__height=height))
        if sport:
            queries.append(Q(profile__sport__icontains=sport))
        if city:
            queries.append(Q(profile__city__icontains=city))
        if sport_time:
            queries.append(Q(profile__sport_time=sport_time))
        if rank is not None:
            rank_value = rank.lower() in ['true', '1', 't', 'y', 'yes']
            queries.append(Q(profile__rank=rank_value))

        if queries:
            query = queries.pop()
            for item in queries:
                query &= item
            queryset = queryset.filter(query)

        return queryset


class DeleteUserView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, username, *args, **kwargs):
        # Find the user by username
        user = get_object_or_404(User, username=username)
        # Delete the user
        user.delete()
        return Response({"message": "User deleted successfully."}, status=204)


class RegistrationStatsView(APIView):
    permission_classes = [IsAdminUser]  # Restrict access to admin users

    def get(self, request, *args, **kwargs):
        today = timezone.now().date()
        month_ago = today - timezone.timedelta(days=30)

        # Count users registered today
        users_today = CustomUser.objects.filter(date_joined__date=today).count()

        # Count users registered in the last week
        users_month = CustomUser.objects.filter(date_joined__date__gte=month_ago).count()

        data = {
            "users_registered_today": users_today,
            "users_registered_past_month": users_month
        }

        serializer = RegistrationStatsSerializer(data=data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDocumentsView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDocumentsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Ensure that only authenticated users can access and modify their documents
        obj, created = UserDocuments.objects.get_or_create(user=self.request.user)
        return obj


class UpdateUserProfileStatusView(generics.UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class AddFavouriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, profile_id):
        user = request.user
        try:
            favourite_profile = UserProfile.objects.get(id=profile_id)
        except UserProfile.DoesNotExist:
            return Response({'error': 'UserProfile not found'}, status=status.HTTP_404_NOT_FOUND)

        if Favourite.objects.filter(user=user, favourite_profile=favourite_profile).exists():
            return Response({'message': 'This profile is already in your favourites'},
                            status=status.HTTP_400_BAD_REQUEST)

        favourite = Favourite(user=user, favourite_profile=favourite_profile)
        favourite.save()
        return Response({'message': 'Profile added to favourites'}, status=status.HTTP_201_CREATED)


class FavouriteListView(generics.ListAPIView):
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)


class SubStatusCreateUpdateView(generics.CreateAPIView, generics.UpdateAPIView):
    queryset = SubStatus.objects.all()
    serializer_class = SubStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user_profile = self.request.user.profile
        substatus = serializer.save(user_profile=user_profile)
        user_profile.status = substatus.message
        user_profile.save()
        return substatus

    def perform_update(self, serializer):
        substatus = serializer.save()
        user_profile = substatus.user_profile
        user_profile.status = substatus.message
        user_profile.save()
        return substatus


class UserDocumentsByUsernameView(generics.RetrieveAPIView):
    serializer_class = UserDocumentsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return get_object_or_404(UserDocuments, user=user)


class AchievementListCreateView(generics.ListCreateAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            user = get_object_or_404(User, username=username)
            return Achievement.objects.filter(user_profile=user.profile)
        return Achievement.objects.filter(user_profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class AchievementDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Achievement.objects.filter(user_profile=self.request.user.profile)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_profile != request.user.profile:
            return Response(
                {"error": "You don't have permission to update this achievement"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_profile != request.user.profile:
            return Response(
                {"error": "You don't have permission to delete this achievement"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class PlaceOfClassesListCreateView(generics.ListCreateAPIView):
    serializer_class = PlaceOfClassesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        if username:
            user = get_object_or_404(User, username=username)
            return PlaceOfClasses.objects.filter(user_profile=user.profile)
        return PlaceOfClasses.objects.filter(user_profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user.profile)


class PlaceOfClassesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlaceOfClassesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PlaceOfClasses.objects.filter(user_profile=self.request.user.profile)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_profile != request.user.profile:
            return Response(
                {"error": "You don't have permission to update this place"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user_profile != request.user.profile:
            return Response(
                {"error": "You don't have permission to delete this place"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)