from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment


TAILWIND_INPUT_CLASSES = 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'

# --- User Registration Form ---

class UserRegistration(UserCreationForm):
    name = forms.CharField(max_length=50, required=True, label='First Name')
    surname = forms.CharField(max_length=50, required=True, label='Last Name')
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Apply Tailwind classes to all fields
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': TAILWIND_INPUT_CLASSES,
                'placeholder': field.label  # Improves UX
            })
    
    class Meta: 
        model = User
        # Include default UserCreationForm fields and add custom fields
        fields = UserCreationForm.Meta.fields + ('name', 'surname', 'email',)
        
    def clean_email(self):
        """Ensures the email address is unique and not already in use."""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        """Saves custom fields (name, surname, email) to the User model."""
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["name"]
        user.last_name = self.cleaned_data["surname"]
        if commit:
            user.save()
        return user

# --- Post Form ---

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to content and emotion_type
        for name, field in self.fields.items():
             field.widget.attrs.update({'class': TAILWIND_INPUT_CLASSES})

    class Meta:
        model = Post
        fields = ['content', 'emotion_type']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'What’s on your mind?'}),
        }

# --- Comment Form ---

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to content
        self.fields['content'].widget.attrs.update({'class': TAILWIND_INPUT_CLASSES})

    class Meta:
        model = Comment
        fields = ['content', 'is_supportive']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Leave a comment...'}),
            # Checkbox input often requires special styling and is left alone here
            'is_supportive': forms.CheckboxInput(), 
        }