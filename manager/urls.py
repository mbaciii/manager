# urls.py
from django.urls import path
from . import views

from .views import custom_login, menu
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from django.contrib import admin
from django.urls import path, include

# urls.py
from django.urls import path
from manager.views import FileUploadView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.manager, name='manager'),
    path('accounts/login/', custom_login, name='custom_login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('menu/', menu, name='menu'),
    path('', include('kasa.urls')),

]
