from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager,PermissionsMixin,)
from django.db import models



class UserManager(BaseUserManager):
    """Manager for User Profile"""

    def create_user(self, email, password=None,):
        """Create a new user"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email,)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email, password=None,):
        """Create a new superuser"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Databse model for users in the system"""

    email = models.EmailField(max_length=100, unique=True)
 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
 
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

    
