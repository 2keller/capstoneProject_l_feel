from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.db.models import Count # New import for cleaner template
from django.views.generic import UpdateView, DeleteView
from .forms import UserRegistration, PostForm, CommentForm
from .models import Post, Profile, Comment, Like, Dislike
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

# --- AUTH VIEWS ---

class SignUpView(View):
    template_name = 'registration/signup.html'

    def get(self, request):
        form = UserRegistration()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistration(request.POST)
        if form.is_valid():
            # Note: Username/email conflict checks removed for conciseness; assume form handles unique fields
            try:
                user = form.save()
                
                # Automatically create profile (critical for preventing 500 errors if template assumes it exists)
                Profile.objects.create(
                    user=user,
                    username=user.username,
                    email=user.email
                )
                
                login(request, user)
                return redirect('feed') # Redirect to feed after signup/login
            except Exception as e:
                logger.error("Signup failed: %s", e)
                form.add_error(None, "Account creation failed. Please check logs.")
        
        return render(request, self.template_name, {'form': form})

# --- CORE VIEWS ---

@login_required # Protects the feed from anonymous access
@login_required
def feed(request):
    # Handle form submission (POST request)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()

    # Annotate posts with counts
    posts = Post.objects.annotate(
        like_count=Count('like', distinct=True),
        dislike_count=Count('dislike', distinct=True),
        comment_count=Count('comment', distinct=True)
    ).order_by('-created_at')

    comment_form = CommentForm()

    return render(request, "core/feed.html", {
        'posts': posts,
        'form': form,
        'comment_form': comment_form,
    })


@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect('feed')

# Like and Dislike views remain clean and functional
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Like.objects.get_or_create(user=request.user, post=post)
    Dislike.objects.filter(user=request.user, post=post).delete()
    return redirect('feed')

@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    Dislike.objects.get_or_create(user=request.user, post=post)
    Like.objects.filter(user=request.user, post=post).delete()
    return redirect('feed')

# --- MANAGEMENT VIEWS ---

class UserPostOwnerMixin(UserPassesTestMixin):
    """Mixin to ensure only the post creator can edit/delete it."""
    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user
        
class EditPostView(LoginRequiredMixin, UserPostOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'core/edit_post.html' # Changed template path to be cleaner
    success_url = reverse_lazy('feed')

class DeletePostView(LoginRequiredMixin, UserPostOwnerMixin, DeleteView):
    model = Post
    template_name = 'core/delete_post.html' # Use a confirmation template
    success_url = reverse_lazy('feed')

# ProfileView remains a placeholder for now
class ProfileView(LoginRequiredMixin, View):
    template_name = 'core/profile.html'
    def get(self, request):
        return render(request, self.template_name, {})