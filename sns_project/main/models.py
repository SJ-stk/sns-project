from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=25, null=True, blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()
    body = models.TextField()
    image = models.ImageField(upload_to="post/", null=True, blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
