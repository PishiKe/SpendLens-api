from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('', include('spendlens.users.urls')),
    path('', include('spendlens.expenses.urls')),
]
