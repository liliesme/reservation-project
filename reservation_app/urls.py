from django.contrib import admin
from django.urls import path,include
from reservation_app import views
from django.contrib.auth import views as auth_views 


urlpatterns = [
  path('', views.base, name='base'),
    path('login', views.auth, name='auth'),
     path('reservation', views.reserver, name='reserver'),
          path('confirmation', views.confirmation, name='confirmation'),
          path('rechercher/', views.rechercher, name='rechercher'),
path('impression/', views.impression, name='impression'),
]
