from django.urls import path
from .views import ProfileListView, PostCreateView, UserProfileView, UpdatePromotionProfileView, \
    UpdateUserProfileView

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('profiles/posts/create/', PostCreateView.as_view(), name='post-create'),
    path('profiles/user/update/', UpdateUserProfileView.as_view(), name='update-user-profile'),
    path('profiles/promotion/update/', UpdatePromotionProfileView.as_view(), name='update-promotion-profile'),
]
