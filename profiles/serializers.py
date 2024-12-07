from rest_framework import serializers

from accounts.serializers import UserProfileSerializer, PromotionProfileSerializer
from .models import Post, Comment, Like, FightRecord
from accounts.models import CustomUser, UserProfile, Favourite, PromotionProfile

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    full_name = serializers.SerializerMethodField()
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'username', 'full_name', 'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def get_full_name(self, obj):
        if hasattr(obj.user, 'profile'):
            return obj.user.profile.full_name
        return None

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if hasattr(obj.user, 'profile') and obj.user.profile.profile_picture and request:
            return request.build_absolute_uri(obj.user.profile.profile_picture.url)
        return None

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'content', 'image', 'video', 'created_at', 'updated_at']
#
#     def validate(self, data):
#         # Check if neither image nor video is provided
#         if not data.get('image') and not data.get('video'):
#             raise serializers.ValidationError("An image or video is required to create a post.")
#         return data

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'video', 'created_at',
                  'updated_at', 'likes_count', 'comments_count', 'is_liked', 'comments', 'author']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def get_author(self, obj):
        profile_picture = None
        request = self.context.get('request')

        if (hasattr(obj.user, 'profile') and
                obj.user.profile.profile_picture and
                request):
            profile_picture = request.build_absolute_uri(obj.user.profile.profile_picture.url)

        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'full_name': obj.user.profile.full_name if hasattr(obj.user, 'profile') else None,
            'profile_picture': profile_picture,
            'is_verified': obj.user.is_verified
        }

class FightRecordSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    approved_status = serializers.SerializerMethodField()

    class Meta:
        model = FightRecord
        fields = ['id', 'status', 'status_display', 'opponent_name', 'promotion',
                  'fight_link', 'weight_category', 'weight', 'is_approved', 'created_at', 'approved_status']

    def get_approved_status(self, obj):
        return "Подтвержден" if obj.is_approved else "На рассмотрении"


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    posts = PostSerializer(many=True, read_only=True, source='user.posts')
    substatus = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_comments = serializers.SerializerMethodField()
    fight_records = serializers.SerializerMethodField()
    fight_stats = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id', 'username', 'full_name', 'birth_date', 'weight', 'height', 'sport', 'city', 'sport_time',
            'profile_picture', 'description', 'rank', 'rank_file', 'video_links', 'instagram_link', 'status',
            'substatus', 'posts', 'is_favourite', 'total_likes', 'total_comments', 'fight_records', 'fight_stats'
        ]
        ref_name = "ProfilesUserProfile"

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.profile_picture.url)
            return obj.profile_picture.url
        return None

    def get_substatus(self, obj):
        latest_substatus = obj.substatuses.order_by('-created_at').first()
        return latest_substatus.message if latest_substatus else obj.status

    def get_is_favourite(self, obj):
        request = self.context.get('request', None)
        if request is None or not request.user.is_authenticated:
            return False
        return Favourite.objects.filter(user=request.user, favourite_profile=obj).exists()

    def get_total_likes(self, obj):
        return Like.objects.filter(post__user=obj.user).count()

    def get_total_comments(self, obj):
        return Comment.objects.filter(post__user=obj.user).count()

    def get_fight_records(self, obj):
        if not obj.user.is_verified:
            return None

        # Get all fight records for verified users, both approved and pending
        records = FightRecord.objects.filter(user_profile=obj).order_by('-created_at')

        # Show all records to the owner and admins, but only approved records to others
        request = self.context.get('request')
        if request:
            if request.user.is_staff or request.user == obj.user:
                return FightRecordSerializer(records, many=True).data
            return FightRecordSerializer(records.filter(is_approved=True), many=True).data

        return FightRecordSerializer(records.filter(is_approved=True), many=True).data

    def get_fight_stats(self, obj):
        if not obj.user.is_verified:
            return None

        # Get approved fight records for verified users
        approved_records = FightRecord.objects.filter(user_profile=obj, is_approved=True)

        # Count wins, losses and ties
        wins = approved_records.filter(status='WIN').count()
        losses = approved_records.filter(status='LOSS').count()
        ties = approved_records.filter(status='TIE').count()

        return f"{wins} - {ties} - {losses}"


class CustomUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)  # This will now include 'status'
    posts = PostSerializer(many=True, read_only=True)
    is_profile_owner = serializers.SerializerMethodField()
    edit_profile_url = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'is_verified', 'is_promotion', 'creator', 'profile', 'posts',
                  'is_profile_owner', 'edit_profile_url']

    def get_is_profile_owner(self, obj):
        # Check if the profile belongs to the current user
        request = self.context.get('request')
        if request and request.user.is_authenticated and obj == request.user:
            return True
        return False

    def get_edit_profile_url(self, obj):
        # Provide the URL to edit the profile only if the current user is the profile owner
        request = self.context.get('request')
        if request and request.user.is_authenticated and obj == request.user:
            return request.build_absolute_uri('/profiles/edit/')
        return None


class VerifiedUserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    full_name = serializers.CharField(source='profile.full_name')
    date_of_birth = serializers.DateField(source='profile.birth_date')
    height = serializers.CharField(source='profile.height')
    weight = serializers.CharField(source='profile.weight')
    sport = serializers.CharField(source='profile.sport')
    profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'height', 'weight', 'sport',
                  'date_of_birth', 'profile_picture']

    def get_username(self, obj):
        return "@" + obj.username

    def get_profile_picture(self, obj):
        request = self.context.get('request')
        if hasattr(obj, 'profile') and obj.profile.profile_picture and request:
            return request.build_absolute_uri(obj.profile.profile_picture.url)
        return None


class CombinedUserProfileSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username', 'phone_number', 'is_verified', 'is_promotion', 'creator', 'profile', 'posts'
        ]

    def get_profile(self, obj):
        user_profile_data = None
        promotion_profile_data = None

        if obj.is_promotion:
            promotion_profile = PromotionProfile.objects.filter(user=obj).first()
            if promotion_profile:
                promotion_profile_data = PromotionProfileSerializer(promotion_profile).data

        user_profile = UserProfile.objects.filter(user=obj).first()
        if user_profile:
            user_profile_data = UserProfileSerializer(user_profile).data

        if promotion_profile_data:
            return {**user_profile_data, **promotion_profile_data} if user_profile_data else promotion_profile_data
        return user_profile_data


