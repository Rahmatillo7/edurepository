from django.views.generic import DetailView, UpdateView
from .models import User
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer

class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    context_object_name = 'profile_user'

    def get_object(self):
        return self.request.user

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['avatar', 'first_name', 'last_name', 'bio', 'telegram_id']
    success_url = '/users/profile/'

    def get_object(self):
        return self.request.user



class UserProfileAPIView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_teacher": user.is_teacher,
            "points": user.points,
            "bio": user.bio,
        }
        return JsonResponse(data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
