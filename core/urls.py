from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from .views import (
    SignUpView,
    feed,
    comment_post,
    like_post,
    dislike_post,
    EditPostView,
    DeletePostView
)

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/homepage.html'), name='home'),
    # Auth routes
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Core app routes
    path('feed/', feed, name='feed'),
    path('post/<int:post_id>/comment/', comment_post, name='comment_post'),
    path('post/<int:post_id>/like/', like_post, name='like_post'),
    path('post/<int:post_id>/dislike/', dislike_post, name='dislike_post'),
    path('post/<int:pk>/edit/', EditPostView.as_view(), name='edit_post'),
    path('post/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),


]