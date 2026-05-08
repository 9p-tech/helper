from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Address


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = ['email', 'username', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email', 'username']
    ordering = ['-date_joined']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'label', 'city', 'state', 'pincode', 'is_default']
    list_filter = ['city', 'state']
    search_fields = ['user__email', 'city', 'pincode']
