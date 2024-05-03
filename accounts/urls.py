# urls.py

from django.urls import path
from .views import RegisterView, UserDetailsUpdateView, UserSportsDetailsUpdateView, LoginView, LogoutView, \
    PromotionUserCreateView, SetUserVerificationView, PaymentView, WaitingVerifiedUsersListView
from .views import PromotionDescriptionView, PromotionRegisterView, PromotionDetailView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = ([
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user-details/', UserDetailsUpdateView.as_view(), name='user-details-update'),
    path('user-sports-details/', UserSportsDetailsUpdateView.as_view(), name='user-sports-details-update'),
    path('promotion-register/', PromotionRegisterView.as_view(), name='promotion-register'),
    path('promotion-description/', PromotionDescriptionView.as_view(), name='promotion-description'),
    path('promotion-detail/', PromotionDetailView.as_view(), name='promotion-detail'),
    path('register-promotion-user/', PromotionUserCreateView.as_view(), name='register-promotion-user'),
    path('set-verification/<int:user_id>/', SetUserVerificationView.as_view(), name='set-verification'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('list-verification/', WaitingVerifiedUsersListView.as_view(), name='list-verification'),

]
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
