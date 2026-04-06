from django.contrib import admin

# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_teacher', 'points', 'is_staff')
    list_editable = ('is_teacher', 'points')
    list_filter = ('is_teacher', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha ma\'lumotlar', {'fields': ('avatar', 'is_teacher', 'points', 'bio', 'telegram_id')}),
    )
