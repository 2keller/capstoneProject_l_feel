from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment

class UserRegistration(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=20)
    surname = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # name and surname are handled manually in the view

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'emotion_type']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'What’s on your mind?'}),
            'emotion_type': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', 'is_supportive']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Leave a comment...'}),
            'is_supportive': forms.CheckboxInput(),
        }

# Optional: ProfileForm for future profile editing
# from .models import Profile
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'surname', 'email', 'bio']
        