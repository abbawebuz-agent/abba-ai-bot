from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('auth/login/', views.CustomTokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('dashboard/', views.dashboard_stats),
    path('users/', views.UserListView.as_view()),
    path('users/<int:pk>/', views.UserDetailView.as_view()),
    path('users/<int:pk>/approve/', views.approve_seller),
    path('users/<int:pk>/reject/', views.reject_seller),
    path('users/bulk-delete/', views.bulk_delete_users),
    path('qr-batches/', views.QRBatchListView.as_view()),
]
