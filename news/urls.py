from django.urls import path
from .views import NewsListView, NewsCreateView, NewsUpdateDeleteView, NewsDetailView

urlpatterns = [
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/update-delete/<int:pk>/', NewsUpdateDeleteView.as_view(), name='news-update-delete'),
]