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


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    first_name = models.CharField(max_length=200, default="First Name")
    last_name = models.CharField(max_length=200, default="Last Name")

    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=20, choices=gender_choices, blank=True, null=True)
    role_choices = (
        ('customer', 'Customer'),
        ('restraurant', 'Restraurant'),
        ('rider', 'Rider'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=15, choices=role_choices, default='customer')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    house_holding_number = models.CharField(max_length=230, null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Staff status (admin)
    is_superuser = models.BooleanField(default=False)  # Superuser status
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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
    def is_restraurant(self):
        return self.role == 'restraurant'

    @property
    def is_customer(self):
        return self.role == 'customer'
    
    @property
    def is_rider(self):
        return self.role == 'rider'
# Default profile image function




    