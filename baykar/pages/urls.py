from django.urls import path, re_path
from pages.views import (
    LoginPageView,
    DashboardPageView,
    UpdatePageView,
    AddPageView
)

app_name = "pages"

urlpatterns = [
    path('', LoginPageView.as_view(), name='login-page'),
    path('dashboard/', DashboardPageView.as_view(), name='dashboard'),
    path('dashboard/<int:pk>/',UpdatePageView.as_view(), name='update-page'),
    path('dashboard/add/', AddPageView.as_view(), name='add')
]
