from django.db import models
from django.utils import timezone

class Expenses(models.Model):
  description = models.CharField(max_length=256, null=True, blank=True)
  date = models.DateTimeField(default=timezone.now)
  amount = models.FloatField(max_length=100, null=True,blank=True)