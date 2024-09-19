from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from core.views import HomeAPIView

schema_view = get_schema_view(
   openapi.Info(
      title="Core API",
      default_version='v1',
      description="Documentation for Core API",
      terms_of_service="https://www.yourcompany.com/terms/",
      contact=openapi.Contact(email="contact@yourcompany.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('accounts.urls')),
    path('', include('profiles.urls')),
    path('news/', include('news.urls')),
    path('home/', HomeAPIView.as_view(), name='home-api'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
