from django.urls import path
from .views import ProfileListView, PostCreateView, UserProfileView, EditUserProfileView

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('posts/create/', PostCreateView.as_view(), name='post-create'),
    path('profiles/edit/', EditUserProfileView.as_view(), name='edit-user-profile'),
]
