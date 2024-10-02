from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User

# Custom admin class
class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff']

    # Define the fields to display in the admin form for viewing/editing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('first_name', 'last_name', 'gender', 'profile_image', 'contact_number')}),
        (_('Address'), {'fields': ('street_address', 'city', 'postal_code', 'house_holding_number')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Role'), {'fields': ('role',)}),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )

    # Fields to display when creating a user (password must be handled differently)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'is_staff', 'is_active')
        }),
    )

    search_fields = ['email', 'first_name', 'last_name']
    filter_horizontal = ('groups', 'user_permissions')

# Register the user model with the custom UserAdmin class
admin.site.register(User, UserAdmin)
