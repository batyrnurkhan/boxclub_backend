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
                            {"id": 1, "title": "Latest Technology Advancements", "content": "Exploring the latest in tech..."},
                            {"id": 2, "title": "Second News", "content": "Content of the second news..."}
                        ],
                        "users_0_57": [
                            {"username": "user1", "weight": 55},
                            {"username": "user2", "weight": 57}
                        ],
                        "users_66_70": [
                            {"username": "user3", "weight": 66},
                            {"username": "user4", "weight": 68}
                        ],
                        "users_94_120": [
                            {"username": "user5", "weight": 94},
                            {"username": "user6", "weight": 120}
                        ],
                        "links": {
                            "full_users_0_57": "http://example.com/accounts/search/?weight_min=0&weight_max=57",
                            "full_users_66_70": "http://example.com/accounts/search/?weight_min=66&weight_max=70",
                            "full_users_94_120": "http://example.com/accounts/search/?weight_min=94&weight_max=120"
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
        def get_users_by_weight(min_weight, max_weight):
            eligible_users = CustomUser.objects.filter(
                is_verified=True,
                profile__weight__gte=min_weight,
                profile__weight__lte=max_weight
            ).prefetch_related('profile').distinct()
            if eligible_users.exists():
                random_users = random.sample(list(eligible_users), min(len(eligible_users), 4))
                serialized_data = VerifiedUserProfileSerializer(random_users, many=True).data
                # Manually add profile pictures if not appearing
                for user_data in serialized_data:
                    user_instance = CustomUser.objects.get(username=user_data['username'].strip('@'))
                    if user_instance.profile:
                        user_data[
                            'profile_picture'] = user_instance.profile.profile_picture.url if user_instance.profile.profile_picture else None
                return serialized_data
            else:
                return []

        # Collect data for all weight ranges
        users_0_65 = get_users_by_weight(0, 65)
        users_66_93 = get_users_by_weight(66, 93)
        users_94_120 = get_users_by_weight(94, 120)

        logger.info(f'Final users_0_65: {users_0_65}')
        logger.info(f'Final users_66_93: {users_66_93}')
        logger.info(f'Final users_94_120: {users_94_120}')

        return Response({
            'latest_news': news_serializer.data,
            'users_0_65': users_0_65,
            'users_66_93': users_66_93,
            'users_94_120': users_94_120,
            'links': {
                'full_users_0_65': request.build_absolute_uri('/accounts/search/?weight_min=0&weight_max=65'),
                'full_users_66_93': request.build_absolute_uri('/accounts/search/?weight_min=66&weight_max=93'),
                'full_users_94_120': request.build_absolute_uri('/accounts/search/?weight_min=94&weight_max=120')
            }
        })
