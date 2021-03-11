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
    path('parks/<int:number>/visit/page', views.visit_park_from_page),
    path('createallparksadmin', views.create_parks),
    path('account', views.account),
    path('account/update', views.update_account),
    path('parks/user/visited', views.visited_parks),
    path('parks/user/leaders', views.leaders),
    path('user/<int:number>/passport', views.user_passport),
    path('parks/random', views.random_park),
    path('parks/user/<int:number>/removevisit', views.remove_visit_from_page),
    path('parks/user/<int:number>/removevisit/home', views.remove_visit),
    path('parks/game', views.parks_game),
    path('parks/game/<int:winner>/<int:loser>', views.rank_park),
    path('parks/ranked', views.display_ranked_parks)
]