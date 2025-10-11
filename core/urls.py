from django.urls import path 
from .views import SignUpView, feed
from  django.contrib.auth import views
from .views import SignUpView

urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('feed/', feed, name='feed'),
    path ('login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', SignUpView.as_view(template_name='registration/signup.html'), name='signup'),
]


