from django.contrib import admin
from .models import Category, Subject, Resource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'subject', 'class_level', 'language', 'is_verified', 'view_count', 'download_count', 'created_at']
    list_filter = ['is_verified', 'language', 'class_level', 'subject']
    search_fields = ['title', 'description', 'author__username']
    list_editable = ['is_verified']
    readonly_fields = ['view_count', 'download_count', 'created_at']
    ordering = ['-created_at']