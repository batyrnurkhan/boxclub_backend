from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    DeleteUserView,
    RegisterView,
    UserDetailsUpdateView,
    UserSportsDetailsUpdateView,
    LoginView,
    LogoutView,
    PromotionUserCreateView,
    SetUserVerificationView,
    PaymentView,
    WaitingVerifiedUsersListView,
    PromotionDescriptionView,
    PromotionRegisterView,
    PromotionDetailView,
    RejectVerificationView,
    VerifiedUsersListView,
    UserSearchListView,
    RegistrationStatsView,
    UpdateUserProfileStatusView,
    AddFavouriteView,
    FavouriteListView,
    UserDocumentsView,
    SubStatusCreateUpdateView,
    UserDocumentsByUsernameView,
    AchievementListCreateView,
    PlaceOfClassesListCreateView, ChangePasswordView, AchievementDetailView,
    AchievementDeleteView, PlaceOfClassesDeleteView, AchievementUpdateView, PlaceOfClassesListView,
    PlaceOfClassesUpdateView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


urlpatterns = [
                  path('accounts/login/', LoginView.as_view(), name='login'),
                  path('accounts/logout/', LogoutView.as_view(), name='logout'),
                  path('accounts/register/', RegisterView.as_view(), name='register'),
                  path('accounts/user-details/', UserDetailsUpdateView.as_view(), name='user-details-update'),
                  path('accounts/user-sports-details/', UserSportsDetailsUpdateView.as_view(),
                       name='user-sports-details-update'),
                  path('accounts/promotion-register/', PromotionRegisterView.as_view(), name='promotion-register'),
                  path('accounts/promotion-description/', PromotionDescriptionView.as_view(), name='promotion-description'),
                  path('accounts/promotion-detail/', PromotionDetailView.as_view(), name='promotion-detail'),
                  path('accounts/register-promotion-user/', PromotionUserCreateView.as_view(), name='register-promotion-user'),
                  path('accounts/set-verification/<str:username>/', SetUserVerificationView.as_view(), name='set-verification'),
                  path('accounts/payment/', PaymentView.as_view(), name='payment'),
                  path('accounts/list-verification/', WaitingVerifiedUsersListView.as_view(), name='list-verification'),
                  path('accounts/reject-verification/<str:username>/', RejectVerificationView.as_view(),
                       name='reject-verification'),
                  path('accounts/verified-users/', VerifiedUsersListView.as_view(), name='verified-users'),
                  path('accounts/search/', UserSearchListView.as_view(), name='users-search'),
                  path('accounts/delete-user/<str:username>/', DeleteUserView.as_view(), name='delete-user'),
                  path('accounts/accounts/registration-stats/', RegistrationStatsView.as_view(), name='registration-stats'),
                  path('accounts/profile/status/', UpdateUserProfileStatusView.as_view(), name='update-profile-status'),

                  path('accounts/user/documents/', UserDocumentsView.as_view(), name='user-documents'),
                  path('accounts/userdocuments/<str:username>/', UserDocumentsByUsernameView.as_view(),
                       name='user-documents-by-username'),

                  path('accounts/substatus/create/', SubStatusCreateUpdateView.as_view(), name='substatus-create'),
                  path('accounts/substatus/<int:pk>/edit/', SubStatusCreateUpdateView.as_view(), name='substatus-edit'),

                  path('accounts/change-password/', ChangePasswordView.as_view(), name='change-password'),

                  path('accounts/profiles/<int:profile_id>/favourite/', AddFavouriteView.as_view(), name='add-favourite'),
                  path('accounts/favourites/', FavouriteListView.as_view(), name='favourite-list'),

                  path('accounts/achievements/',
                       AchievementListCreateView.as_view(),
                       name='achievement-list-create'),

                  path('accounts/places-of-classes/',
                       PlaceOfClassesListCreateView.as_view(),
                       name='place-of-classes-list-create'),

                  path('accounts/places-of-classes/<str:username>/',
                       PlaceOfClassesListView.as_view(),
                       name='place-of-classes-list'),

                  # Update by ID
                  path('accounts/places-of-classes/update/<int:pk>/',
                       PlaceOfClassesUpdateView.as_view(),
                       name='place-of-classes-update'),

                  # Delete by ID
                  path('accounts/places-of-classes/<int:pk>/',
                       PlaceOfClassesDeleteView.as_view(),
                       name='place-of-classes-delete'),

                  path('accounts/achievements/<str:username>/',
                       AchievementDetailView.as_view(),
                       name='achievement-detail'),

                path('accounts/achievements/update/<int:pk>/',
                     AchievementUpdateView.as_view(),
                     name='achievement-update'),

                  # Delete by ID
                  path('accounts/achievements/<int:pk>/',
                       AchievementDeleteView.as_view(),
                       name='achievement-delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
