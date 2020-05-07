"""PICO_PROJECT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from . import views
from core.views import ProfileView, ChargeView, MyPicoLog
from core.views import follow, FollowersView, FollowingView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
    re_path(r'^accounts/register/activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),

    path('', views.HomeView.as_view(), name='home'),
    path('explore/', include('photo.urls')),
    path('charge/', ChargeView.as_view(), name='charge'),
    path('search/', views.post_search, name='search'),
    path('log/user/<str:username>', MyPicoLog.as_view(), name='mypicolog'),
    # path('log/photo/<int:pk>', name='photopicolog'),
    path('<str:username>/', ProfileView.as_view(), name='profile'),
    path('<str:username>/follow/', follow, name='follow'),
    path('<str:username>/followers', FollowersView.as_view(), name='followers'),
    path('<str:username>/following', FollowingView.as_view(), name='following'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
