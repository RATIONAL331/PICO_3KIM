from django.urls import path
from . import views

app_name = 'photo'
urlpatterns = [
    # 기본 explore은 day의 rank와 같다.
    path('', views.PhotoLV.as_view(), name='index'),

    path('week/', views.PhotoLVRankWeek.as_view(), name='rank_week'),
    path('month/', views.PhotoLVRankMonth.as_view(), name='rank_month'),
    path('3month/', views.PhotoLVRank3Month.as_view(), name='rank_3month'),
    path('year/', views.PhotoLVRankYear.as_view(), name='rank_year'),
    path('all/', views.PhotoLVRankAll.as_view(), name='rank_all'),

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
