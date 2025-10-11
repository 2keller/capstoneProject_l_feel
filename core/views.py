from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView
from .forms import ProfileForm, UserRegistration

class SignUpView(CreateView):
    user_form = UserRegistration
    template_name = 'signup.html'
    profile_form = ProfileForm
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.user_form()
        profile_form = self.profile_form()
        return render(request, self.template_name, {'user_form': form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        form = self.user_form(request.POST)
        profile_form = self.profile_form(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template_name, {'user_form': form, 'profile_form': profile_form})


# Create your views here
def feed(request):
    post = Post.objects.all()
    return render(request,"feed.html", {'post':post})

