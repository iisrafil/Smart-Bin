"""DigitalDustbin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from api.views import data_list, device_info, user_handle, notification
from landing.views import home, auth_login, logout_view, device_list, add_device, update_device, view_device, \
    delete_device, user_list, update_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', data_list, name="data_api"),
    path('api/device/', device_info, name="device_api"),
    path('api/user/', user_handle, name="user_api"),
    path('api/notify/', notification, name="notification_api"),
    path('', home, name="home"),
    path("login/", auth_login, name='login'),
    path("logout/", logout_view, name='logout'),
    path("device/all/", device_list, name='device_list'),
    path("device/add/", add_device, name='add_device'),
    path("device/<id>/", view_device, name='view_device'),
    path("device/<id>/update/", update_device, name='update_device'),
    path("device/<id>/delete/", delete_device, name='delete_device'),
    path("user/all/", user_list, name='user_list'),
    path("user/<id>/update/", update_user, name='update_user'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
