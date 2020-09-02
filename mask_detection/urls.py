"""mask_detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

import hogist
from hogist import urls
from accounts import views

urlpatterns = [
    path('django/admin/login/', admin.site.urls),
    path('', include(hogist.urls)),
    path('client/login/', views.user_login, name='login'),
    path('admin/signup/', views.signup, name='signup'),
    path('admin/admin_login/', views.admin_login, name='admin-login'),
    path('admin/admin_index/', views.admin_index, name='admin-index'),
    path('admin/admin_userlist/', views.admin_UserList, name='admin_userlist'),
    path('admin/admin_list/', views.admin_list, name='admin_list'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('admin/admin_setting/', views.admin_setting, name='admin_setting'),
]
