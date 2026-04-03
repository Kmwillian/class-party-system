from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_full_name', 'is_class_rep', 'is_active')
    list_filter = ('is_class_rep', 'is_active', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Class Rep Info', {'fields': ('phone_number', 'is_class_rep')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')