from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import login
from django.db.models import Count
from django.views.generic import UpdateView, DeleteView
from .forms import UserRegistration, PostForm, CommentForm
from .models import Post, Profile, Comment, Like, Dislike
from django.contrib.auth.models import User
from django.contrib import messages # New Import for user feedback
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
            try:
                user = form.save()
                
                # Automatically create profile
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

# ----------------------------------------------------------------------
# --- CORE VIEWS ---
# ----------------------------------------------------------------------

@login_required
def feed(request):
    """Handles both displaying the feed (GET) and creating a post (POST)."""
    
    # 1. Handle form submission (POST request)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # Success: Add message and use PRG pattern
            messages.success(request, "Your post was successfully shared!")
            return redirect('feed')
        else:
            # Failure: Add message, but DO NOT redirect. 
            # Fall through to rendering with the error-bound form.
            messages.error(request, "Post could not be submitted. Please correct the errors below.")
    else:
        # 2. Initialize fresh PostForm for GET request
        form = PostForm()

    # 3. Always fetch all necessary template context data (regardless of POST or GET)
    posts = Post.objects.annotate(
        like_count=Count('like', distinct=True),
        dislike_count=Count('dislike', distinct=True),
        comment_count=Count('comment', distinct=True)
    ).order_by('-created_at')

    comment_form = CommentForm() # Always needed for comments section

    # 4. Render the template
    return render(request, "core/feed.html", {
        'posts': posts,
        'form': form, # Form instance (either fresh or with validation errors)
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


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Use get_or_create to ensure idempotency (no duplicate likes)
    Like.objects.get_or_create(user=request.user, post=post)
    # Ensure any previous dislike is removed
    Dislike.objects.filter(user=request.user, post=post).delete()
    return redirect('feed')


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Use get_or_create to ensure idempotency
    Dislike.objects.get_or_create(user=request.user, post=post)
    # Ensure any previous like is removed
    Like.objects.filter(user=request.user, post=post).delete()
    return redirect('feed')

# ----------------------------------------------------------------------
# --- MANAGEMENT VIEWS ---
# ----------------------------------------------------------------------

class UserPostOwnerMixin(UserPassesTestMixin):
    """Mixin to ensure only the post creator can edit/delete it."""
    def test_func(self):
        post = self.get_object()
        return post.user == self.request.user
        
class EditPostView(LoginRequiredMixin, UserPostOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'core/edit_post.html'
    success_url = reverse_lazy('feed')

class DeletePostView(LoginRequiredMixin, UserPostOwnerMixin, DeleteView):
    model = Post
    template_name = 'core/delete_post.html'
    success_url = reverse_lazy('feed')

class ProfileView(LoginRequiredMixin, View):
    template_name = 'core/profile.html'
    def get(self, request):
        return render(request, self.template_name, {})
    
def home(request):
    return render(request, 'core/homepage.html')