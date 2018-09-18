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
from problem import views

urlpatterns = [
    url(r'^set_problem/', views.set_problem),
    url(r'^recommend_list/', views.recommend_list),
    url(r'^comment/', views.comment),
    url(r'^comment_list/', views.comment_list),
    url(r'^hot_list/', views.hot_list),
    url(r'^collection/', views.collection),
    url(r'^collection_list/', views.collection_list),
    url(r'^follow_member/', views.follow_member),
    url(r'^my_follow/', views.my_follow),
    url(r'^private_letter/', views.private_letter),
    url(r'^set_private_letter/', views.set_private_letter),
    url(r'^message/', views.message),
    url(r'^recent_browse/', views.recent_browse),
    url(r'^fabulous/', views.fabulous),
    url(r'^follow_list/', views.follow_list),
    url(r'^set_answer/', views.set_answer),
    url(r'^dynamic_message/', views.dynamic_message),
    url(r'^details/', views.details),
    url(r'^search/', views.search),
    url(r'^delete_collection/', views.delete_collection),
]
