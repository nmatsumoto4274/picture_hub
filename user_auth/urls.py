import django.contrib.auth.views
from django.urls import path

from user_auth import views

app_name = 'user_auth'

urlpatterns = [
    path('top/', views.top_page, name="top"),  # リダイレクト
    path('login/',  # ログイン
         django.contrib.auth.views.LoginView.as_view(template_name='user_auth/login.html'),
         name='login'),
    path('logout/',  # ログアウト
         django.contrib.auth.views.LogoutView.as_view(template_name='user_auth/login.html'),
         name='logout'),
]
