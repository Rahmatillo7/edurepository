from django.urls import path
from .views import UserProfileView, UserProfileUpdateView, UserProfileAPIView, RegisterView

app_name = 'users'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='profile_edit'),
    path('profil', UserProfileAPIView.as_view(), name='profile'),

    path('register/', RegisterView.as_view(), name='auth_register'),
]
