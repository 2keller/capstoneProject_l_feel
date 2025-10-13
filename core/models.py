from django.db import models
from django.contrib.auth.models import User

# Emotion choices
emotion_type = [
    ('happy', 'happy'),
    ('sad', 'sad'),
    ('angry', 'angry'),
    ('surprise', 'surprise'),
    ('fear', 'fear'),
    ('neutral', 'neutral'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    bio = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Post(models.Model):
    content = models.TextField()
    emotion_type = models.CharField(max_length=100, choices=emotion_type)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    is_supportive = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} on Post {self.post.id}: {self.content[:30]}"#type:ignore

    class Meta:
        ordering = ['-created_at']

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"#type: ignore

    class Meta:
        unique_together = ('user', 'post')

class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} disliked Post {self.post.id}"#type:ignore

    class Meta:
        unique_together = ('user', 'post')
