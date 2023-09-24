from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
import uuid
# Create your models here.

class User_Model(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, required=True)
    username = models.CharField(max_length=255, required=True)
    email = models.EmailField(max_length=254, verbose_name='Email', required=True)
    role = models.IntegerField(choices=[(0, 'User'), (1, 'Admin')], default=0, verbose_name='role', required=True)
    state = models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=1, verbose_name='status', required=True)
    password = models.CharField(max_length=128, required=True)
    
    def __str__(self):
    	return f'{self.username}'

class Certificate(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, required=True)
    arabic_data = models.JSONField(verbose_name='Arabic Certificate', required=True)
    national_id_name = models.CharField(max_length=255, required=True)
    user = models.ForeignKey(User_Model, on_delete=models.CASCADE, required=True)
    
    def __str__(self):
        return self.national_id_name


class UserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have a Email')

        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')

        user = self.create_user(username, email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, required=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    role = models.IntegerField(choices=[(0, 'User'), (1, 'Admin')], default=0, verbose_name='role', required=True)
    REQUIRED_FIELDS = ['username', 'email']

    objects = UserManager()

    def _str_(self):
        return self.email