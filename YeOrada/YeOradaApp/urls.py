from django.urls import path

from YeOradaApp import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('clientprofile', views.clientprofile, name='clientprofile'),
    path('settings', views.settings, name='settings'),
]