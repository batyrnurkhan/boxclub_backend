from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from accounts.models import CustomUser, UserProfile, PromotionProfile
from .models import Post, Like, FightRecord
from .serializers import UserProfileSerializer, PostSerializer, CustomUserSerializer, CombinedUserProfileSerializer, \
    PromotionProfileSerializer, CommentSerializer, FightRecordSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied


class ProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all().select_related('user').prefetch_related('user__posts')
    serializer_class = UserProfileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


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

class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to delete this post.")
        return obj

class PostUpdateView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to update this post.")
        return obj


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            like, created = Like.objects.get_or_create(user=request.user, post=post)

            if not created:
                like.delete()
                return Response({'status': 'unliked'})
            return Response({'status': 'liked'})
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class PostCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            serializer = CommentSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user, post=post)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.prefetch_related('comments', 'likes').all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class FightRecordCreateView(generics.CreateAPIView):
    serializer_class = FightRecordSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_verified:
            raise PermissionDenied("Only verified users can add fight records.")
        serializer.save(user_profile=self.request.user.profile)

class FightRecordListView(generics.ListAPIView):
    serializer_class = FightRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FightRecord.objects.filter(
            user_profile__user__username=self.kwargs.get('username'),
            user_profile__user__is_verified=True,
            is_approved=True
        )


class UnapprovedFightRecordListView(generics.ListAPIView):
    serializer_class = FightRecordSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return FightRecord.objects.filter(
            is_approved=False,
            user_profile__user__is_verified=True
        ).select_related('user_profile__user').order_by('-created_at')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)