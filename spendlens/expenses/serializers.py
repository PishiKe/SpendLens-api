from rest_framework import serializers
from . import models

class ExpensesSerializer(serializers.ModelSerializer):
  class Meta:
    model = models.Expenses
    fields = '__all__'
