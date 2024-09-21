from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group, Permission
# from purchase.models import Order

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password=password, **extra_fields)

    

def default_profile_image():
    return "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_960_720.png"

# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    first_name = models.CharField(max_length=200, default="First Name")
    last_name = models.CharField(max_length=200, default="Last Name")
    profile_image = models.ImageField(upload_to='profile_images/', default=default_profile_image, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=6, choices=gender_choices, blank=True, null=True)
    role_choices = (
        ('customer', 'Customer'),
        ('restraurant', 'Restraurant'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=15, choices=role_choices, default='customer')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Staff status (admin)
    is_superuser = models.BooleanField(default=False)  # Superuser status

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser  # Superusers have all permissions

    def has_module_perms(self, app_label):
        return self.is_superuser  # Superusers have module-level permissions

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_rider(self):
        return self.role == 'restraurant'

    @property
    def is_customer(self):
        return self.role == 'customer'
# Default profile image function




    