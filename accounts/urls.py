# urls.py

from django.urls import path
from .views import RegisterView, UserDetailsUpdateView, UserSportsDetailsUpdateView, LoginView, LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user-details/', UserDetailsUpdateView.as_view(), name='user-details-update'),
    path('user-sports-details/', UserSportsDetailsUpdateView.as_view(), name='user-sports-details-update'),
]
