from django.urls import path
from . import views

app_name = 'photo'
urlpatterns = [
    # 기본 explore은 day의 rank와 같다.
    path('', views.PhotoLV.as_view(), name='index'),

    # path('rank/week/', ,name='rank_week'),
    # path('rank/month/', ,name='rank_month'),
    # path('rank/3month', ,name='rank_3month'),
    # path('rank/year/', ,name='rank_year'),
    # path('rank/all/', ,name='rank_all'),

    path('follow/', views.PhotoFollowView.as_view(), name='follow'),
    path('<int:pk>/', views.PhotoDV.as_view(), name='photo_detail'),

    path('add/', views.PhotoCV.as_view(), name='photo_add'),
    path('change/', views.PhotoChangeLV.as_view(), name='photo_change'),
    path('<int:pk>/update/', views.PhotoUV.as_view(), name='photo_update'),
    path('<int:pk>/delete/', views.PhotoDelV.as_view(), name='photo_delete'),

    path('<int:pk>/donate', views.PhotoDonateDetailView.as_view(), name='photo_donate'),
    path('<int:pk>/log', views. PhotoPicoLog.as_view(), name='photo_pico_log'),

    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
] 
