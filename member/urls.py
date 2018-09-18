"""thing_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from member import views

urlpatterns = [
    url(r'^$', views.login),
    url(r'^index/', views.index),
    url(r'^phone_register/', views.phone_register),
    url(r'^login/$', views.login),
    url(r'^register_code/', views.register_code),
    url(r'^set_member/', views.set_member),
    url(r'^forget_password/', views.forget_password),
    url(r'^verification/', views.verification),
    url(r'^pwd_verify_code/', views.pwd_verify_code),
    url(r'^update_pwd/', views.update_pwd),
    url(r'^login_quick/', views.login_quick),
    url(r'^login_out/', views.login_out),
]
