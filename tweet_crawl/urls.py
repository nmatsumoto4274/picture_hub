from django.urls import path
import django.contrib.auth.views as django_views

from tweet_crawl import views

app_name = 'tweet_crawl'

urlpatterns = [
    path('top/', views.top, name="top"),
    path('logout/', django_views.LogoutView.as_view(template_name='tweet_crawl/logout.html'), name='logout'),
]
