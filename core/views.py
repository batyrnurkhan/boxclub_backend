from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.models import CustomUser
from profiles.serializers import VerifiedUserProfileSerializer
from news.serializers import NewsSerializer
from news.models import News
import random

class HomeAPIView(APIView):
    def get(self, request):
        # Get the latest news
        latest_news = News.objects.latest('id')
        news_serializer = NewsSerializer(latest_news)

        # Helper function to get random verified users by weight range
        def get_users_by_weight(min_weight, max_weight):
            eligible_users = CustomUser.objects.filter(
                is_verified=True,
                profile__weight__gte=min_weight,
                profile__weight__lte=max_weight
            )
            random_users = random.sample(list(eligible_users), min(len(eligible_users), 4))
            return VerifiedUserProfileSerializer(random_users, many=True).data

        # Collect data for all weight ranges
        users_0_57 = get_users_by_weight(0, 57)
        users_66_70 = get_users_by_weight(66, 70)
        users_94_120 = get_users_by_weight(94, 120)

        return Response({
            'latest_news': news_serializer.data,
            'users_0_57': users_0_57,
            'users_66_70': users_66_70,
            'users_94_120': users_94_120,
            'links': {
                'full_users_0_57': request.build_absolute_uri('/accounts/search/?weight_min=0&weight_max=57'),
                'full_users_66_70': request.build_absolute_uri('/accounts/search/?weight_min=66&weight_max=70'),
                'full_users_94_120': request.build_absolute_uri('/accounts/search/?weight_min=94&weight_max=120')
            }
        })