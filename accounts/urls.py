from django.urls import path
from .views import (
    RegisterView,
    UserDetailsUpdateView,
    UserSportsDetailsUpdateView,
    LoginView,
    LogoutView,
    PromotionUserCreateView,  # Assuming this is for creating promotional users and profiles
    SetUserVerificationView,
    PaymentView,
    WaitingVerifiedUsersListView,
    PromotionDescriptionView,
    PromotionRegisterView,
    PromotionDetailView,
    RejectVerificationView, VerifiedUsersListView, UserSearchListView,
)

from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user-details/', UserDetailsUpdateView.as_view(), name='user-details-update'),
    path('user-sports-details/', UserSportsDetailsUpdateView.as_view(), name='user-sports-details-update'),
    path('promotion-register/', PromotionRegisterView.as_view(), name='promotion-register'),  # Handles creation of new promotional profiles
    path('promotion-description/', PromotionDescriptionView.as_view(), name='promotion-description'),
    path('promotion-detail/', PromotionDetailView.as_view(), name='promotion-detail'),
    path('register-promotion-user/', PromotionUserCreateView.as_view(), name='register-promotion-user'),  # Create promotional user and associated profile
    path('set-verification/<int:user_id>/', SetUserVerificationView.as_view(), name='set-verification'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('list-verification/', WaitingVerifiedUsersListView.as_view(), name='list-verification'),
    path('reject-verification/<int:user_id>/', RejectVerificationView.as_view(), name='reject-verification'),
    path('verified-users/', VerifiedUsersListView.as_view(), name='verified-users'),
    path('search/', UserSearchListView.as_view(), name='users-search'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
