from . import views
from django.urls import path

urlpatterns = [
    path('', views.login),
    path('home', views.homepage),
    path('register', views.register),
    path('login', views.login),
    path('userlogin', views.userlogin),
    path('hike/finder', views.hike_finder)
]