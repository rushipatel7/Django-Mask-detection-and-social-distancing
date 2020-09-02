from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here

class admin_details(models.Model):
    username = models.CharField(max_length=15)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'admin_details'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


# class MyUser(AbstractUser):
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.BooleanField(default=True)
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     email = models.EmailField(verbose_name='email', max_length=100, unique=True)
#     is_staff = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
#     company_name = models.CharField(max_length=30)
#     mobile_no = models.CharField(max_length=15)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']
#
#     def __str__(self):
#         return self.email
#
#     def has_perm(self, perm, Object=None):
#         return self.is_superuser
#
#     def has_module_perm(self, perm, Object=None):
#         return True


# class extendUser(models.Model):
#     company_name = models.CharField(max_length=30)
#     mobile_number = models.CharField(max_length=15)
#     # user = models.OneToOneField(User,on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'User_Extra_Info'

class extendUserDetails(models.Model):
    email = models.CharField(max_length=30)
    company_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, blank=True)



    class Meta:
        managed = False
        db_table = 'extend_user_info'

# class userIpdetails(models.Model):
#     ip_address = models.GenericIPAddressField()
#     with_mask_count = models.IntegerField()
#     without_mask_count = models.IntegerField()
#
#     class Meta:
#         db_table = 'User_IPDetails'