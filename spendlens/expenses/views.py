from rest_framework import viewsets
from . import serializers
from . import models

class ExpenseViewset(viewsets.ModelViewSet):
    serializer_class = serializers.ExpenseSerializer
    queryset = models.Expense.objects.all()
