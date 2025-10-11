from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
    

class Profile(models.Model):
    User = models.OneToOneField(models.Model, verbose_name=_(""), on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    



emotion_type = [
    ('happy', 'happy'),
    ('sad', 'sad'),
    ('angry', 'angry'),
    ('surprise', 'surprise'),
    ('fear', 'fear'),
    ('neutral', 'neutral'),
]
class Post(models.Model):
    content = models.TextField()
    emotion_type = models.CharField(max_length=100, choices=emotion_type)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
    
class comment (models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_supportive = models.BooleanField(default=True)

    def __str__(self):
        return self.content
    


class like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    
class dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
    
