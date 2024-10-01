from django.db import models
from django.utils import timezone
from spendlens.common.models import Currency
from django.contrib.auth import get_user_model

class Expense(models.Model):
  name = models.CharField(max_length=256, null=True, blank=True)
  description = models.CharField(max_length=256, null=True, blank=True)
  date = models.DateTimeField(default=timezone.now)
  amount = models.FloatField(max_length=100, null=True,blank=True)
  currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
  user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

  class Meta:
    verbose_name = 'Expense'
    verbose_name_plural = 'Expenses'

  def __str__(self):
    return self.description

class Budget(models.Model):
  name = models.CharField(max_length=256, null=True, blank=True)
  description = models.CharField(max_length=256, null=True, blank=True)
  amount = models.FloatField(max_length=100, null=True,blank=True)
  currency = models.ForeignKey(Currency, on_delete=models.PROTECT, blank=True, null=True)
  user = models.ForeignKey(get_user_model(), on_delete=models.PROTECT)

  class Meta:
    verbose_name = 'Budget'
    verbose_name_plural = 'Budgets'

  def __str__(self):
    return self.description

