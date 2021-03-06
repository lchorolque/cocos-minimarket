from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
import environ
#  apps urls
from backend.stores.urls import urlpatterns as stores_viewsets

env = environ.Env()

schema_view = get_schema_view(
   openapi.Info(
      title="Backend Template Service API",
      default_version='1.0.0',
      description="API REST for Template Service",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="leandrochorolque@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/stores/', include(stores_viewsets))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if env('ENVIRONMENT') == 'development':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
