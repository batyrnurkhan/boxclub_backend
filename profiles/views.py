from rest_framework import viewsets, permissions, generics
from rest_framework.generics import CreateAPIView
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


class EditUserProfileView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def get_object(self):
        # Ensure users can only edit their own profile
        return self.request.user