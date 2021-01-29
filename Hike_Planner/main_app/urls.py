from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('register/data', views.registerdata),
    path('login', views.login),
    path('userlogin', views.userlogin),
    path('parks', views.parks),
    path('parks/allparks', views.allparks),
    path('logout', views.logout,),
    path('parks/<int:number>', views.park_by_number),
    path('parks/<int:number>/visit', views.visit_park),
    path('createallparksadmin', views.create_parks),
    path('account', views.account),
    path('account/update', views.update_account),
    path('parks/user/visited', views.visited_parks),
    path('parks/user/leaders', views.leaders),
    path('user/<int:number>/passport', views.user_passport)
]