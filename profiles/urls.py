from django.urls import path
from .views import ProfileListView, PostCreateView, UserProfileView, UpdatePromotionProfileView, \
    UpdateUserProfileView, PostUpdateView, PostDeleteView, PostLikeView, PostCommentView, PostDetailView, \
    FightRecordListView, FightRecordCreateView, UserFightRecordView

urlpatterns = [
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('profiles/<str:username>/', UserProfileView.as_view(), name='user-profile'),
    path('profiles/posts/create/', PostCreateView.as_view(), name='post-create'),
    path('profiles/user/update/', UpdateUserProfileView.as_view(), name='update-user-profile'),
    path('profiles/posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('profiles/posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('profiles/promotion/update/', UpdatePromotionProfileView.as_view(), name='update-promotion-profile'),
    path('profiles/posts/<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
    path('profiles/posts/<int:pk>/comment/', PostCommentView.as_view(), name='post-comment'),
    path('profiles/posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('profiles/<str:username>/fights/', UserFightRecordView.as_view()),
    path('profiles/fights/create/', FightRecordCreateView.as_view()),
]
