from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('list', views.UserViewSet, 'users')
router.register('groups', views.GroupViewSet, 'groups')
router.register('permissions', views.PermissionViewSet, 'permissions')

urlpatterns = [
    path('password_reset/', views.PasswordResetView.as_view()),
    path('password_reset_confirm/', views.ResetPassword.as_view()),
    path('password_change/', views.ChangePassword.as_view()),
    path('verify_account/', views.VerifyAccountRequest.as_view()),
    path('verify_account_confirm/', views.VerifyAccountConfirm.as_view()),
    path('me/', views.UserAuthenticated.as_view()),
    path('group_user/', views.GroupUser.as_view()),
    path('group_permissions/', views.GroupPermission.as_view()),
] + router.urls
