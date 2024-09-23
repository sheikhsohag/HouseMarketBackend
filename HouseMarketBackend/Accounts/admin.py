from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Sections to organize the form layout
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'profile_image', 'address', 'gender')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Role Info'), {'fields': ('role',)}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    # Fields when creating a new user (i.e., no password entered yet)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'is_staff', 'is_superuser'),
        }),
    )

    # Admin page settings for better customization
    filter_horizontal = ('groups', 'user_permissions',)

# Register the custom UserAdmin
admin.site.register(User, UserAdmin)
