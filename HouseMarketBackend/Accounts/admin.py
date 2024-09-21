from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    # Define the forms for adding and changing users
    add_form = UserCreationForm
    form = UserChangeForm

    # The fields to be used in displaying the User model.
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role')

    fieldsets = (
        (None, 
         {'fields': ('email', 'password')}),
         
        ('Personal Info', {'fields': ('first_name', 'last_name', 'profile_image', 'address', 'gender', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    # Fields shown when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()

    # Override save_model to hash the password
    def save_model(self, request, obj, form, change):
        if form.is_valid() and form.cleaned_data.get('password1'):
            # This ensures that the password is hashed
            obj.set_password(form.cleaned_data.get('password1'))
        super().save_model(request, obj, form, change)

# Register the User model with the custom UserAdmin
admin.site.register(User, UserAdmin)
