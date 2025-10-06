from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm







#login views and user registartion views 
def register(request):
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')

            return redirect('login')
    else:
        return render(request, 'core/register.html', {'form': form, 'title': 'register here'})


def Login(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        User = authenticate(request, username = username, password = password)
        if User is not None:
            form = login(request, User)

            return redirect('feed.html')
        else:
            #message
            form = AuthenticationForm
            return render(request, 'login.html', {'form':form})










# Create your views here
def feed(request):
    post = Post.objects.all()
    render(request,"feed.html", {'post':post})

