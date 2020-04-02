from django.urls import path
from .views import UserCreateView, UserLoginView, UserLogoutView

urlpatterns = [
    path('v1/user/create/', UserCreateView.as_view(), name='apis_v1_user_create'),
    path('v1/user/login/', UserLoginView.as_view(), name='apis_v1_user_login'),
    path('v1/user/logout/', UserLogoutView.as_view(), name='apis_v1_user_logout'),
]
