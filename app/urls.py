from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('movie_details/', views.movie_details, name='movie_details'),
    
    path('movies/<slug:slug>/', views.movie_details, name="movie_details"),
    path('tvshows/<slug:slug>/', views.tvshows_details, name='tvshows_details'), 


]
