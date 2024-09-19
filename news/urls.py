from django.urls import path, re_path
from .views import NewsListView, NewsCreateView, NewsUpdateDeleteView, NewsDetailView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.conf import settings
from django.conf.urls.static import static
schema_view = get_schema_view(
   openapi.Info(
      title="News API",
      default_version='v1',
      description="API documentation for News endpoints",
      terms_of_service="https://www.yourcompany.com/terms/",
      contact=openapi.Contact(email="contact@yourcompany.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)


urlpatterns = [
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/create/', NewsCreateView.as_view(), name='news-create'),
    path('news/<int:pk>/', NewsDetailView.as_view(), name='news-detail'),
    path('news/update-delete/<int:pk>/', NewsUpdateDeleteView.as_view(), name='news-update-delete'),

    # Swagger and ReDoc paths

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
