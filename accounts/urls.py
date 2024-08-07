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
    PlaceOfClassesListCreateView, ChangePasswordView
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Accounts API",
        default_version='v1',
        description="API documentation for Accounts app",
        terms_of_service="https://www.yourcompany.com/terms/",
        contact=openapi.Contact(email="contact@yourcompany.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('user-details/', UserDetailsUpdateView.as_view(), name='user-details-update'),
                  path('user-sports-details/', UserSportsDetailsUpdateView.as_view(),
                       name='user-sports-details-update'),
                  path('promotion-register/', PromotionRegisterView.as_view(), name='promotion-register'),
                  path('promotion-description/', PromotionDescriptionView.as_view(), name='promotion-description'),
                  path('promotion-detail/', PromotionDetailView.as_view(), name='promotion-detail'),
                  path('register-promotion-user/', PromotionUserCreateView.as_view(), name='register-promotion-user'),
                  path('set-verification/<str:username>/', SetUserVerificationView.as_view(), name='set-verification'),
                  path('payment/', PaymentView.as_view(), name='payment'),
                  path('list-verification/', WaitingVerifiedUsersListView.as_view(), name='list-verification'),
                  path('reject-verification/<str:username>/', RejectVerificationView.as_view(),
                       name='reject-verification'),
                  path('verified-users/', VerifiedUsersListView.as_view(), name='verified-users'),
                  path('search/', UserSearchListView.as_view(), name='users-search'),
                  path('delete-user/<str:username>/', DeleteUserView.as_view(), name='delete-user'),
                  path('accounts/registration-stats/', RegistrationStatsView.as_view(), name='registration-stats'),
                  path('profile/status/', UpdateUserProfileStatusView.as_view(), name='update-profile-status'),

                  path('user/documents/', UserDocumentsView.as_view(), name='user-documents'),
                  path('userdocuments/<str:username>/', UserDocumentsByUsernameView.as_view(),
                       name='user-documents-by-username'),

                  path('substatus/create/', SubStatusCreateUpdateView.as_view(), name='substatus-create'),
                  path('substatus/<int:pk>/edit/', SubStatusCreateUpdateView.as_view(), name='substatus-edit'),

                  path('change-password/', ChangePasswordView.as_view(), name='change-password'),

                  path('profiles/<int:profile_id>/favourite/', AddFavouriteView.as_view(), name='add-favourite'),
                  path('favourites/', FavouriteListView.as_view(), name='favourite-list'),
                  path('achievements/', AchievementListCreateView.as_view(), name='achievement-list-create'),
                  path('places-of-classes/', PlaceOfClassesListCreateView.as_view(), name='place-of-classes-list-create'),
                  re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
