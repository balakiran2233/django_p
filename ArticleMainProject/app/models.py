from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(User, related_name = 'likes')
    created_date = models.DateField(max_length=50, auto_now_add=True)
    updated_date = models.DateField(max_length=50, auto_now=True)

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.id, self.slug])

    def total_likes(self):
        return self.likes.count()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    photo = models.ImageField(null=True, blank=True)

class Images(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)             # Many to One
    image = models.ImageField(upload_to='images/', blank=True, null=True)


class CommentData(models.Model):
    comment = models.CharField(max_length=200)
    date = models.DateField()