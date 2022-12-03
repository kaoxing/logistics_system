"""logistics_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from app01 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user_login/', views.user_login),
    path('poster_login/', views.poster_login),
    path('manager_login/', views.manager_login),
    path("home/", views.home),
    path("poster_index/", views.poster_index),
    path("user_index/", views.user_index),
    path("poster_setting/", views.poster_setting),
    path("map/", views.map)
]
