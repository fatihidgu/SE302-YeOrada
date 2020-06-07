from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static

from YeOradaApp import views

urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),
    path('home', views.index, name='home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('clientprofile/<str:username>', views.clientprofile, name='clientprofile'),
    path('settings', views.settings, name='settings'),
    path('clientsearch', views.clientsearch, name='clientsearch'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('myprofile', views.myprofile, name='myprofile'),
    path('likeComment', views.likeComment, name='likeComment'),
    path('clientsettings', views.clientsettings, name='clientsettings'),
    path('adminsettings', views.adminsettings, name='adminsettings'),
    path('adminprofile', views.adminprofile, name='adminprofile'),
    path('newclient', views.newclient, name='newclient'),
    path('faq', views.faq, name='faq'),
    path('forgotpassword', views.forgotpassword, name='forgotpassword'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)