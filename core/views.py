from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from adminfunc.models import ProbableFight
from adminfunc.serializers import ProbableFightSerializer
from news.serializers import NewsSerializer
from news.models import News
from profiles.models import Post
from profiles.serializers import VerifiedUserProfileSerializer, PostSerializer
import random
import logging
from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)

class PostPagination(PageNumberPagination):
    page_size = 10
    max_page_size = 10
    page_size_query_param = 'page_size'


class HomeAPIView(APIView):
    pagination_class = PostPagination

    def get(self, request):
        # Initialize paginator
        paginator = self.pagination_class()

        # Get latest posts from verified users
        latest_posts = Post.objects.filter(
            user__is_verified=True
        ).select_related(
            'user',
            'user__profile'
        ).prefetch_related(
            'comments',
            'comments__user',
            'comments__user__profile',
            'likes'
        ).order_by('-created_at')

        # Paginate posts
        paginated_posts = paginator.paginate_queryset(latest_posts, request)
        posts_serializer = PostSerializer(paginated_posts, many=True, context={'request': request})

        # Get all news, ordered by latest first
        all_news = News.objects.all().order_by('-id')
        news_serializer = NewsSerializer(all_news, many=True)

        # Helper function to get random verified users by weight range
        def get_users_by_weight(min_weight, max_weight=None):
            if max_weight:
                eligible_users = CustomUser.objects.filter(
                    is_verified=True,
                    profile__weight__gte=min_weight,
                    profile__weight__lte=max_weight
                ).prefetch_related('profile').distinct()
            else:
                eligible_users = CustomUser.objects.filter(
                    is_verified=True,
                    profile__weight__gte=min_weight
                ).prefetch_related('profile').distinct()

            if eligible_users.exists():
                random_users = random.sample(list(eligible_users), min(len(eligible_users), 4))
                serialized_data = VerifiedUserProfileSerializer(random_users, many=True).data
                for user_data in serialized_data:
                    user_instance = CustomUser.objects.get(username=user_data['username'].strip('@'))
                    if user_instance.profile and user_instance.profile.profile_picture:
                        user_data['profile_picture'] = request.build_absolute_uri(
                            user_instance.profile.profile_picture.url)
                    else:
                        user_data['profile_picture'] = None
                return serialized_data
            else:
                logger.info(f"No users found for weight range {min_weight} - {max_weight}")
                return []

        # Collect data for weight ranges
        users_0_65 = get_users_by_weight(0, 145)  # Сверхлегкие бойцы
        users_66_93 = get_users_by_weight(146, 170)  # Легкие бойцы
        users_94_120 = get_users_by_weight(171)  # Бойцы тяжеловесы

        probable_fights = ProbableFight.objects.all().order_by('-created_at')[:5]  # Get latest 5 fights
        probable_fights_serializer = ProbableFightSerializer(probable_fights, many=True)

        # Get pagination information
        pagination_data = {
            'count': paginator.page.paginator.count,
            'next': paginator.get_next_link(),
            'previous': paginator.get_previous_link(),
            'current_page': paginator.page.number,
            'total_pages': paginator.page.paginator.num_pages,
        }

        return Response({
            'latest_posts': {
                'results': posts_serializer.data,
                'pagination': pagination_data
            },
            'latest_news': news_serializer.data,
            'users_0_65': users_0_65,
            'users_66_93': users_66_93,
            'users_94_120': users_94_120,
            'probable_fights': probable_fights_serializer.data,
            'links': {
                'full_users_0_65': request.build_absolute_uri('/accounts/search/?weight_min=0&weight_max=145'),
                'full_users_66_93': request.build_absolute_uri('/accounts/search/?weight_min=146&weight_max=170'),
                'full_users_94_120': request.build_absolute_uri('/accounts/search/?weight_min=171')
            }
        })


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import UserProfile
from accounts.serializers import UserProfileSerializer
from django.db.models import Q, F, ExpressionWrapper, IntegerField
from django.db.models.functions import ExtractYear, Now
from django.utils import timezone


class UserProfileSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Get search parameters from request.GET
        city = request.GET.get('city', '')
        full_name = request.GET.get('full_name', '')
        sport = request.GET.get('sport', '')
        weight_min = request.GET.get('weight_min')
        weight_max = request.GET.get('weight_max')
        height_min = request.GET.get('height_min')
        height_max = request.GET.get('height_max')
        age_min = request.GET.get('age_min')
        age_max = request.GET.get('age_max')
        status = request.GET.get('status', '')  # Added status parameter

        # Start with all profiles
        profiles = UserProfile.objects.all()

        # Apply filters based on the provided parameters
        if city:
            profiles = profiles.filter(city__icontains=city)
        if full_name:
            profiles = profiles.filter(full_name__icontains=full_name)
        if sport:
            profiles = profiles.filter(sport__icontains=sport)

        # Add status filter
        if status:
            profiles = profiles.filter(status__iexact=status)

        if weight_min:
            try:
                profiles = profiles.filter(weight__gte=int(weight_min))
            except ValueError:
                pass
        if weight_max:
            try:
                profiles = profiles.filter(weight__lte=int(weight_max))
            except ValueError:
                pass

        # For height, since it's a CharField, ensure heights are numeric and compare as integers
        if height_min:
            try:
                height_min_int = int(height_min)
                profiles = profiles.filter(height__regex=r'^\d+$').filter(
                    height__gte=str(height_min_int))
            except ValueError:
                pass
        if height_max:
            try:
                height_max_int = int(height_max)
                profiles = profiles.filter(height__regex=r'^\d+$').filter(
                    height__lte=str(height_max_int))
            except ValueError:
                pass

        # Annotate profiles with calculated age
        profiles = profiles.filter(birth_date__isnull=False).annotate(
            age=ExpressionWrapper(
                ExtractYear(Now()) - ExtractYear('birth_date'),
                output_field=IntegerField()
            )
        )

        if age_min:
            try:
                profiles = profiles.filter(age__gte=int(age_min))
            except ValueError:
                pass
        if age_max:
            try:
                profiles = profiles.filter(age__lte=int(age_max))
            except ValueError:
                pass

        # Serialize the profiles
        serializer = UserProfileSerializer(profiles, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)