from . import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('register/data', views.registerdata),
    path('login', views.login),
    path('userlogin', views.userlogin),
    path('parks', views.parks),
    path('parks/guest', views.parks_guest),
    path('parks/allparks', views.allparks),
    path('parks/allparks/', views.allparks, name='all_parks'),
    path('parks/allparks/guest', views.allparks_guest),
    path('logout', views.logout,),
    path('parks/<int:number>', views.park_by_number),
    path('parks/<int:number>/guest', views.park_by_number_guest),
    path('parks/<int:number>/visit', views.visit_park),
    path('parks/<int:number>/visit/page', views.visit_park_from_page),
    path('createallparksadmin', views.create_parks),
    path('account', views.account, name='account'),
    path('account/update', views.update_account),
    path('parks/user/visited', views.visited_parks),
    path('parks/user/leaders', views.leaders),
    path('user/<int:number>/passport', views.user_passport),
    path('parks/random', views.random_park),
    path('parks/user/<int:number>/removevisit', views.remove_visit_from_page),
    path('parks/user/<int:number>/removevisit/home', views.remove_visit),
    path('parks/game', views.parks_game),
    path('parks/game/<int:winner>/<int:loser>', views.rank_park),
    path('parks/ranked', views.display_ranked_parks),
    path('admin', views.admin),
    path('admin/deleteuser/<int:user_id>', views.delete_user)
]