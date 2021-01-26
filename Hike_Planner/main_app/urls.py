from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('home', views.homepage),
    path('register', views.register),
    path('register/data', views.registerdata),
    path('login', views.login),
    path('userlogin', views.userlogin),
    path('hike/finder', views.hike_finder),
    path('logout', views.logout,)
]