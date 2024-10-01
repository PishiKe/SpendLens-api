from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from spendlens.common.models import Currency

GenderChoices = [
  ('Male', 'Male'),
  ('Female', 'Female'),
  ('n/a', 'n/a')
]

class UserManager(BaseUserManager):
  use_in_migrations = True

  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('The given email must be set')

    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)

    if extra_fields.get('is_staff') is not True:
      raise ValueError('Superuser must have is_staff=True.')
    if extra_fields.get('is_superuser') is not True:
      raise ValueError('Superuser must have is_superuser=True.')

    return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
  username = models.CharField(max_length=64, unique=True)
  email= models.EmailField(_('email address'), unique=True)
  verified = models.BooleanField(default=False)
  phone = models.CharField(max_length=15, blank=True, null=True)
  gender = models.CharField(max_length=10, blank=True, choices=GenderChoices)
  currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)

  objects = UserManager()

  def __str__(self):
    return self.username

  @property
  def full_name(self):
    return f"{self.first_name} {self.last_name}"

  @property
  def is_admin(self):
    return True if self.is_superuser or self.is_staff else False