from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction

from .models import Post, Comment, Like, Dislike
from .forms import PostForm, CommentForm, UserRegistration


class ModelsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass12345')

    def test_post_str_and_ordering(self):
        Post.objects.create(user=self.user, content='First', emotion_type='happy')
        Post.objects.create(user=self.user, content='Second', emotion_type='sad')
        posts = list(Post.objects.all())
        self.assertEqual(posts[0].content, 'Second')  # Ordered by -created_at
        self.assertIn('alice:', str(posts[0]))

    def test_comment_str_and_ordering(self):
        post = Post.objects.create(user=self.user, content='Hello', emotion_type='neutral')
        Comment.objects.create(user=self.user, post=post, content='First comment')
        Comment.objects.create(user=self.user, post=post, content='Second comment')
        comments = list(Comment.objects.all())
        self.assertEqual(comments[0].content, 'Second comment')
        self.assertIn('alice', str(comments[0]))

    def test_like_and_dislike_uniqueness(self):
        post = Post.objects.create(user=self.user, content='Test', emotion_type='angry')
        Like.objects.create(user=self.user, post=post)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Like.objects.create(user=self.user, post=post)

        Dislike.objects.create(user=self.user, post=post)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Dislike.objects.create(user=self.user, post=post)


class FormsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bob', password='pass12345')

    def test_post_form_valid(self):
        form = PostForm(data={'content': 'Feeling great', 'emotion_type': 'happy'})
        self.assertTrue(form.is_valid())

    def test_comment_form_valid(self):
        form = CommentForm(data={'content': 'Nice post!', 'is_supportive': True})
        self.assertTrue(form.is_valid())

    def test_user_registration_email_unique(self):
        User.objects.create_user(username='charlie', password='pass12345', email='c@example.com')
        form = UserRegistration(data={
            'username': 'newuser',
            'password1': 'aStrongP4ssword!',
            'password2': 'aStrongP4ssword!',
            'name': 'New',
            'surname': 'User',
            'email': 'c@example.com',  # duplicate
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_registration_saves_names(self):
        form = UserRegistration(data={
            'username': 'dora',
            'password1': 'aStrongP4ssword!',
            'password2': 'aStrongP4ssword!',
            'name': 'Dora',
            'surname': 'Explorer',
            'email': 'd@example.com',
        })
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.first_name, 'Dora')
        self.assertEqual(user.last_name, 'Explorer')
        self.assertEqual(user.email, 'd@example.com')


class ViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='eve', password='pass12345')

    def test_homepage_ok(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_feed_requires_login(self):
        resp = self.client.get(reverse('feed'))
        self.assertEqual(resp.status_code, 302)  # redirect to login
        self.assertIn('/login', resp.url)

    def test_create_post_via_feed(self):
        self.client.login(username='eve', password='pass12345')
        resp = self.client.post(reverse('feed'), data={'content': 'posting', 'emotion_type': 'happy'})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Post.objects.filter(user=self.user).count(), 1)

    def test_comment_like_dislike_flow(self):
        self.client.login(username='eve', password='pass12345')
        post = Post.objects.create(user=self.user, content='topic', emotion_type='sad')

        # comment
        resp = self.client.post(reverse('comment_post', args=[post.id]), data={'content': 'support', 'is_supportive': True})
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Comment.objects.filter(post=post).count(), 1)

        # like idempotent, removes dislike
        self.client.get(reverse('dislike_post', args=[post.id]))
        self.client.get(reverse('like_post', args=[post.id]))
        self.client.get(reverse('like_post', args=[post.id]))
        self.assertEqual(Like.objects.filter(user=self.user, post=post).count(), 1)
        self.assertEqual(Dislike.objects.filter(user=self.user, post=post).count(), 0)

