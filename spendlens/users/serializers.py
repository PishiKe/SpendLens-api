from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from .models import CustomUser
from django.db import transaction
from dj_rest_auth.registration.serializers import RegisterSerializer

class PermissionSerializer(serializers.ModelSerializer):
  app = serializers.CharField(source='content_type.app_label', read_only=True)
  model = serializers.CharField(source='content_type.model', read_only=True)

  class Meta:
    model = Permission
    fields = ['id', 'name', 'app', 'model']


class GroupSerializer(serializers.ModelSerializer):
  permissions = PermissionSerializer(many=True, read_only=True)
  class Meta:
    model = Group
    fields = ['name', 'id', 'permissions']


class UsersSlimSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ['id', 'first_name', 'last_name', 'email', 'username', 'is_admin']


class UserSerializer(serializers.ModelSerializer):
  groups = GroupSerializer(many=True, read_only=True)

  class Meta:
    model = CustomUser
    fields = [
        'id', 'first_name', 'last_name', 'email', 'username', 'phone', 'gender', 'is_staff', 'is_superuser', 'is_admin', 'is_active', 'last_login', 'groups',
    ]



class UserRegistrationSerializer(RegisterSerializer):

  first_name = serializers.CharField(max_length=50)
  last_name = serializers.CharField(max_length=50)

  @transaction.atomic
  def save(self, request):
      user = super().save(request)
      user.first_name = self.data.get('first_name')
      user.last_name = self.data.get('last_name')
      user.username = self.data.get('username')
      user.save()
      return user

