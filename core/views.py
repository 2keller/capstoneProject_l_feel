
from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse_lazy
from .forms import UserRegistration, ProfileForm
from .models import Post

class SignUpView(View):
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')

    def get(self, request):
        user_form = UserRegistration()
        profile_form = ProfileForm()
        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

    def post(self, request):
        user_form = UserRegistration(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'user_form': user_form,
            'profile_form': profile_form,
        })

def feed(request):
    post = Post.objects.all()
    return render(request, "feed.html", {'post': post})