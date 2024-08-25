from rest_framework import viewsets
from . import serializers
from . import models

class ExpensesViewset(viewsets.ModelViewSet):
  serializer_class = serializers.EspensesSerializer
  queryset = models.Expenses.objects.all()
