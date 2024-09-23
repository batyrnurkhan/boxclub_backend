from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from news.serializers import NewsSerializer
from news.models import News
from profiles.serializers import VerifiedUserProfileSerializer
import random
import logging

logger = logging.getLogger(__name__)


class HomeAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve all news articles and a selection of verified users by weight category.",
        responses={
            200: openapi.Response(
                description="A collection of news articles and user profiles by weight category",
                examples={
                    "application/json": {
                        "latest_news": [
                            {"id": 1, "title": "Latest Technology Advancements",
                             "content": "Exploring the latest in tech..."},
                            {"id": 2, "title": "Second News", "content": "Content of the second news..."}
                        ],
                        "super_lightweight_fighters": [
                            {"username": "user1", "weight": 125},
                            {"username": "user2", "weight": 135}
                        ],
                        "lightweight_fighters": [
                            {"username": "user3", "weight": 155},
                            {"username": "user4", "weight": 170}
                        ],
                        "heavyweight_fighters": [
                            {"username": "user5", "weight": 185},
                            {"username": "user6", "weight": 205}
                        ],
                        "links": {
                            "full_super_lightweight_fighters": "http://example.com/accounts/search/?weight_min=0&weight_max=145",
                            "full_lightweight_fighters": "http://example.com/accounts/search/?weight_min=146&weight_max=170",
                            "full_heavyweight_fighters": "http://example.com/accounts/search/?weight_min=171"
                        }
                    }
                }
            )
        }
    )
    def get(self, request):
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
                    if user_instance.profile:
                        user_data[
                            'profile_picture'] = user_instance.profile.profile_picture.url if user_instance.profile.profile_picture else None
                return serialized_data
            else:
                return []

        # Collect data for weight ranges
        super_lightweight_fighters = get_users_by_weight(0, 145)  # Сверхлегкие бойцы
        lightweight_fighters = get_users_by_weight(146, 170)  # Легкие бойцы
        heavyweight_fighters = get_users_by_weight(171)  # Бойцы тяжеловесы

        logger.info(f'Super lightweight fighters: {super_lightweight_fighters}')
        logger.info(f'Lightweight fighters: {lightweight_fighters}')
        logger.info(f'Heavyweight fighters: {heavyweight_fighters}')

        return Response({
            'latest_news': news_serializer.data,
            'users_0_65': super_lightweight_fighters,
            'users_66_93': lightweight_fighters,
            'users_94_120': heavyweight_fighters,
            'links': {
                'full_users_0_65': request.build_absolute_uri('/accounts/search/?weight_min=0&weight_max=145'),
                'full_users_66_93': request.build_absolute_uri('/accounts/search/?weight_min=146&weight_max=170'),
                'full_users_94_120': request.build_absolute_uri('/accounts/search/?weight_min=171')
            }
        })
