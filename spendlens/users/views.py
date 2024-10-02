from rest_framework import viewsets, views, filters
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django_filters.rest_framework import DjangoFilterBackend
from . import serializers
from . import models
import secrets

class UserViewSet(viewsets.ModelViewSet):
  serializer_class = serializers.UserSerializer
  queryset = models.CustomUser.objects.all()
  filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
  filter_fields = ['email', 'first_name', 'last_name', 'groups__name']
  search_fields = ['email', 'first_name', 'last_name', 'groups__name']
  ordering_fields = ['id']
  # permission_classes = [IsAuthenticated]

  @action(detail=True, methods=['PATCH'])
  def makeAdmin(self, request, pk):
    if(request.user == 'AnonymousUser'):
      return Response(data='Not Authenticated', status=401)

    authedUser = get_user_model().objects.get(email=request.user)
    if not authedUser.is_staff:
      return Response(data='Not Authorized', status=401)

    user = self.get_object()
    user.is_staff = not user.is_staff
    user.save()
    return Response(serializers.UserSerializer(user).data, status=200)

class PermissionViewSet(viewsets.ModelViewSet):
  serializer_class = serializers.PermissionSerializer
  queryset = Permission.objects.all()


class GroupViewSet(viewsets.ModelViewSet):
  serializer_class = serializers.GroupSerializer
  queryset = Group.objects.all()
  # permission_classes = [IsAuthenticated]


class UserAuthenticated(views.APIView):
  def get(self, request):
    # print(type(request.user))
    if request.user.is_anonymous:
      return Response(data='Not Authenticated', status=401)
    else:
      serialized = serializers.UserSerializer(request.user)
      return Response(serialized.data, status=200)


class GroupUser(views.APIView):

  def post(self, request):
    data = request.data
    user =  get_user_model().objects.filter(pk=data['user']).first()
    if user:
      group = Group.objects.filter(pk=data['group']).first()
      if group:
        user.groups.add(group)
        return Response({
            'data': {'message': 'User added to group successfully'},
            'status': status.HTTP_200_OK
        })
      else:
        return Response({
            'data': {'message': f"The group id: {data['group']} does not exist."},
            'status': status.HTTP_400_BAD_REQUEST
        })
    else:
      return Response({
        'data': {'message': f"The user id: {data['user']} does not exist."},
        'status': status.HTTP_400_BAD_REQUEST
      })

  def delete(self, request):
    data = request.data
    user =  get_user_model().objects.filter(pk=data['user']).first()
    if user:
      group = Group.objects.filter(pk=data['group']).first()
      if group:
        user.groups.remove(group)
        return Response({
            'data': {'message': 'User removed from group successfully'},
            'status': status.HTTP_200_OK
        })
      else:
        return Response({
            'data': {'message': f"The group id: {data['group']} does not exist."},
            'status': status.HTTP_400_BAD_REQUEST
        })
    else:
      return Response({
          'data': {'message': f"The user id: {data['user']} does not exist."},
          'status': status.HTTP_400_BAD_REQUEST
      })

class GroupPermission(views.APIView):

  def post(self, request):
      data = request.data

      group = Group.objects.get(pk=data['group'])
      permission = Permission.objects.get(pk=data['permission'])
      group.permissions.add(permission)

      return Response(data="Permission added to group successfully", status=200)

  def delete(self, request):
      data = request.data
      group = Group.objects.get(pk=data['group'])
      permission = Permission.objects.get(pk=data['permission'])
      group.permissions.remove(permission)

      return Response(data="Permission removed from group successfully", status=200)


class PasswordResetView(views.APIView):

  def post(self, request):
      data = request.data

      users = get_user_model().objects.filter(username=data['username'])
      if users.count() == 1:
          models.PassResetToken.objects.create(
              token=secrets.token_hex(32),
              user=users[0]
          )
          return Response(data="Check Your Email for a link.", status=201)
      else:
          return Response(data={"message": f"The username {data['username']} does not exist."}, status=400)


class ResetPassword(views.APIView):

  def post(self, request):
    data = request.data

    try:
      token = models.PassResetToken.objects.get(
          token=data['token'])
      if token and token.is_valid():
        user = get_user_model().objects.get(pk=token.user.pk)
        if user:
          user.password = make_password(data['password'])
          user.save()
          token.reset = True
          token.save()
          return Response(data="Your Password has been reset", status=201)
        else:
          return Response(data={"message":f"The email {data['email']} does not exist."}, status=400)
      return Response(data={"message": f"The link has expired or is invalid."}, status=400)
    except Exception as e:
      return Response(data={"message": "The link has expired or is invalid."}, status=400)

class ChangePassword(views.APIView):

    def post(self, request):
      data = request.data
      try:
        user = get_user_model().objects.get(pk=data['id'])

        if user:
          user.password = make_password(data['password'])
          user.save()
          return Response(data="Your Password has been reset", status=201)
        else:
          return Response(data=f"The email {data['email']} does not exist.", status=400)
      except:
        return Response(data=f"Id and password are required.", status=400)


class VerifyAccountRequest(views.APIView):

    def post(self, request):
      data = request.data
      user = get_user_model().objects.get(email=data['email'])
      if user:
        if user.verified is not True:
          models.VerifyToken.objects.create(
            token=secrets.token_hex(32),
            user=user
          )
          return Response(data="Check Your Email for a link", status=201)
        else:
          return Response(data="Your Account is already verified!", status=200)
      else:
        return Response(data=f"The email {data['email']} does not exist.", status=400)


class VerifyAccountConfirm(views.APIView):

  def post(self, request):
    data = request.data
    token = models.VerifyToken.objects.filter(
        token=data['token'], user__email=data['email']).order_by('-id')[0]
    if token and token.is_valid():
      user = get_user_model().objects.get(email=data['email'])
      if user:
        user.verified = True
        user.save()
        token.verified = True
        token.save()
        return Response(data="Your Account has been verified!", status=201)
      else:
        return Response(data=f"The email {data['email']} does not exist.", status=400)
    return Response(data=f"The link has expired or is invalid.", status=400)