from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import UserRegistrationView
from rest_framework.authtoken import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="BirthdayGreetings API",
      default_version='v1',
      description="api docs",
      contact=openapi.Contact(email="borzikovu32@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-token-auth/', views.obtain_auth_token),
    path('register/', UserRegistrationView.as_view(), name='register_user'),
    path('', include(router.urls)),
]
