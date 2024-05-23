from django.urls import path
from .views import ProfileListView, CurrentUserProfileView

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profile/', CurrentUserProfileView.as_view(), name='current-user-profile'),
]
