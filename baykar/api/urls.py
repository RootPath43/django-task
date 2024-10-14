from django.urls import path, re_path
from api.views import (
    LoginAPIView,
    DashboardAPIView,
    DeleteAndUpdateAPIView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Baykar API",
        default_version='v1',
        description="Baykar API description",
        terms_of_service="",
        contact=openapi.Contact(email="emirhan.gulgorr@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


app_name = "api"

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login-api'),
    path('dashboard/', DashboardAPIView.as_view(),
         name="dashboard-api"),
    path('dashboard/<int:pk>/', DeleteAndUpdateAPIView.as_view(),
         name='delete-and-update'),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]
