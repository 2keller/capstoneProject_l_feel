from django.urls import path 
from .views import SignUpView, feed
from  django.contrib.auth import views


urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('feed/', feed, name='feed'), 
  
]
