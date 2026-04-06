from django.urls import path
from .views import ResourceListAPIView, ResourceDetailAPIView, ResourceCreateAPIView, ResourceDownloadAPIView

app_name = 'resources'

urlpatterns = [
    path('', ResourceListAPIView.as_view(), name='list'),
    path('<int:pk>/', ResourceDetailAPIView.as_view(), name='detail'),
    path('create/', ResourceCreateAPIView.as_view(), name='create'),

    path('<int:pk>/download/', ResourceDownloadAPIView.as_view(), name='download'),

]