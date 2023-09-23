from django.db import models
from django.contrib.auth.models import  BaseUserManager, AbstractBaseUser

# Create your models here.


class NewUserManager(BaseUserManager):
    def create_user(self, email, fname ,lname,tc,mobileNumber, password=None ,password2=None):
        """
        Creates and saves a User with the given email, name ,tc,mobileNumber and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            fname = fname,
            lname = lname,
            mobileNumber=mobileNumber,
            tc = tc
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,  fname ,lname,tc,mobileNumber, password=None):
        """
        Creates and saves a superuser with the given email, fname ,lname,tc, and password.
        """
        user = self.create_user(
            email,
            password=password,
            fname = fname,
            lname = lname,
            mobileNumber=mobileNumber,
            tc = tc
        )
        user.is_admin = True
        user.save(using=self._db)
        return user






class NewUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email address',
        max_length=255,
        unique=True,
    )
    fname = models.CharField( verbose_name='First Name',max_length=100)
    lname = models.CharField(verbose_name='last Name',max_length=100,default="")
    mobileNumber = models.CharField(verbose_name='Mobile Number',max_length=30 ,default="")
    tc = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    social_login = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    objects = NewUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname' ,'lname' ,'mobileNumber','tc']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
