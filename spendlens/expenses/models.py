from django.db import models
from django.utils import timezone

class Expenses(models.Model):
  name = models.CharField(max_length=256, null=True, blank=True)
  description = models.CharField(max_length=256, null=True, blank=True)
  date = models.DateTimeField(default=timezone.now)
  amount = models.FloatField(max_length=100, null=True,blank=True)

  class Meta:
    verbose_name = 'Expense'
    verbose_name_plural = 'Expenses'

  def __str__(self):
    return self.description
