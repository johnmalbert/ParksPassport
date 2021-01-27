from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('register/data', views.registerdata),
    path('login', views.login),
    path('userlogin', views.userlogin),
    path('parks', views.parks),
    path('logout', views.logout,),
    path('parks/<int:number>', views.park_by_number),
    path('createallparksadmin', views.create_parks)
]