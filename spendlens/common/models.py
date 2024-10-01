from django.db import models

class Currency(models.Model):
  name = models.CharField(max_length=50, unique=True)

  class Meta:
    verbose_name = 'Currency'
    verbose_name_plural = 'Currencies'

  def __str__(self):
    return self.name