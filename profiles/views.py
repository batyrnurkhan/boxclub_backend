from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser, UserProfile, PromotionProfile
from .models import Post
from .serializers import UserProfileSerializer, PostSerializer, CustomUserSerializer, CombinedUserProfileSerializer, PromotionProfileSerializer
from rest_framework.response import Response


class ProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all().select_related('user').prefetch_related('user__posts')
    serializer_class = UserProfileSerializer


class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    lookup_field = 'username'
    serializer_class = CombinedUserProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        username = self.kwargs.get(self.lookup_field)
        user = self.get_queryset().filter(username=username).first()

        if not user:
            raise NotFound("User not found.")

        serializer = self.get_serializer(user)
        return Response(serializer.data)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.views import APIView
from rest_framework import status, permissions

class UpdateUserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if request.user.is_promotion:
            return Response({"error": "Not allowed for promotion profiles"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserProfileSerializer(request.user.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)


class UpdatePromotionProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if not request.user.is_promotion:
            return Response({"error": "Not applicable for non-promotion profiles"}, status=status.HTTP_400_BAD_REQUEST)

        profile, created = PromotionProfile.objects.get_or_create(user=request.user)
        serializer = PromotionProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

