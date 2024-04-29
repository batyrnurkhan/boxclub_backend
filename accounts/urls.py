# urls.py

from django.urls import path
from .views import RegisterView, UserDetailsUpdateView, UserSportsDetailsUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('user-details/<int:pk>/', UserDetailsUpdateView.as_view(), name='user-details-update'),
    path('user-sports-details/<int:pk>/', UserSportsDetailsUpdateView.as_view(), name='user-sports-details-update'),
]
