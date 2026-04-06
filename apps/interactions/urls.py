from django.urls import path
from .views import add_comment, toggle_favorite

app_name = 'interactions'

urlpatterns = [
    path('comment/<int:resource_id>/', add_comment, name='add_comment'),
    path('favorite/<int:resource_id>/', toggle_favorite, name='toggle_favorite'),
]
