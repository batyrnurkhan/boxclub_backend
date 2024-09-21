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
    url='/api/',
)

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include('profiles.urls')),
    path('api/', include('news.urls')),
    path('api/home/', HomeAPIView.as_view(), name='home-api'),
                  re_path(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
                          name='schema-json'),
                  re_path(r'^api/swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                  re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)