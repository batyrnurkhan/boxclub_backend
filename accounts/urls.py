# urls.py

from django.urls import path
from .views import RegisterView, UserDetailsUpdateView, UserSportsDetailsUpdateView, LoginView, LogoutView
from .views import PromotionDescriptionView, PromotionRegisterView, PromotionDetailView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user-details/', UserDetailsUpdateView.as_view(), name='user-details-update'),
    path('user-sports-details/', UserSportsDetailsUpdateView.as_view(), name='user-sports-details-update'),
    path('promotion-register/', PromotionRegisterView.as_view(), name='promotion-register'),
    path('promotion-description/', PromotionDescriptionView.as_view(), name='promotion-description'),
    path('promotion-detail/', PromotionDetailView.as_view(), name='promotion-detail')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
