from django.conf import settings
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static

from YeOradaApp import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('clientprofile/<str:username>', views.clientprofile, name='clientprofile'),
    path('settings', views.settings, name='settings'),
    path('clientsearch', views.clientsearch, name='clientsearch'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('myprofile', views.myprofile, name='myprofile'),
    path('likeComment', views.likeComment, name='likeComment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)