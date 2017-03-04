from __future__ import unicode_literals

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, username, password=None):
        user = self.model(username=username, is_staff=False,
                          is_active=True, is_superuser=False)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'

    username = models.CharField(max_length=20, unique=True, db_index=True)

    first_name = models.CharField(
        max_length=10, null=True, blank=True, default=None)
    last_name = models.CharField(
        max_length=50, null=True, blank=True, default=None)
    email = models.EmailField(null=True, blank=True, default=None)
    can_create_contest = models.BooleanField(default=False)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def __unicode__(self):
        if not self.first_name or not self.last_name:
            return 'user %s' % (str(self.id))
        return '%s %s' % (self.last_name, self.first_name)
