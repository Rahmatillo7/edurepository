from django.contrib import admin
from .models import Comment, Favorite, Report

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'text', 'created_at']
    search_fields = ['text', 'user__username']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'reason']
    search_fields = ['reason', 'user__username']