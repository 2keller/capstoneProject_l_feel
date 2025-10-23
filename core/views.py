from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegistration, PostForm, CommentForm
from .models import Post, Profile, Comment, Like, Dislike
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
import logging
from django.contrib.auth import login



logger = logging.getLogger(__name__)

class SignUpView(View):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def get(self, request):
        form = UserRegistration()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserRegistration(request.POST)
        if form.is_valid():
            try:
                User.objects.get(email=form.cleaned_data['email'])
                form.add_error('email', 'This email is already in use.')
                return render(request, self.template_name, {'form': form})
            except User.DoesNotExist:
                pass

            try:
                User.objects.get(username=form.cleaned_data['username'])
                form.add_error('username', 'This username is already taken.')
                return render(request, self.template_name, {'form': form})
            except User.DoesNotExist:
                pass
            try:
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.save()

            # Automatically create profile
                Profile.objects.create(
                    user=user,
                    username = form.cleaned_data['username'],
                    email=form.cleaned_data['email']
                )

                
                login(request, user)
                return redirect('home')
            except Exception as e:
                logger.error("Signup failed: %s", e)
                form.add_error(None, "Something went wrong. Please try again later.")

        return render(request, self.template_name, {'form': form})



def feed(request):
    posts = Post.objects.all()
    form = PostForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feed')

    return render(request, "core/feed.html", {
        'posts': posts,
        'form': form,
        'comment_form': comment_form
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
    existing_like = Like.objects.filter(user=request.user, post=post)
    if not existing_like.exists():
        # Remove dislike if it exists
        Dislike.objects.filter(user=request.user, post=post).delete()
        Like.objects.create(user=request.user, post=post)
    return redirect('feed')


@login_required
def dislike_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    existing_dislike = Dislike.objects.filter(user=request.user, post=post)
    if not existing_dislike.exists():
        # Remove like if it exists
        Like.objects.filter(user=request.user, post=post).delete()
        Dislike.objects.create(user=request.user, post=post)
    return redirect('feed')

class EditPostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'edit_post.html'
    success_url = reverse_lazy('feed')

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class DeletePostView(LoginRequiredMixin, View):
    success_url = reverse_lazy('feed')

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)
        post.delete()
        return redirect(self.success_url)
class ProfileView(LoginRequiredMixin, View):
    template_name = 'core/profile.html'

    