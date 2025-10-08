from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm















# Create your views here
def feed(request):
    post = Post.objects.all()
    render(request,"feed.html", {'post':post})

