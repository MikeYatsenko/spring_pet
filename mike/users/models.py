from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AnonymousUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have name')
        if email is None:
            raise TypeError('Please specify correct email')

        user = self.model(username=username, email = self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have name')
        if password is None:
            raise TypeError('Please specify correct password')
        if email is None:
            raise TypeError('Please specify correct email')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    REDACTOR = 1
    READER = 2

    ROLE_CHOICES = (
        (REDACTOR, 'Redactor'),
        (READER, 'Reader')
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    username = models.CharField(max_length=225, unique=True, db_index=True)
    email = models.EmailField(max_length=50, unique=True, db_index=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=2)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }