from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    pass

class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    website = models.CharField(max_length=30)
    search = models.CharField(max_length=64)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} searched {self.search} on {self.website} ({self.id})"
    
class Article(models.Model):
    headline = models.CharField(max_length=256)
    body = models.CharField(max_length=5000)
    category = models.CharField(max_length=32)
    url = models.URLField(max_length=200)
    search = models.ForeignKey(Query, on_delete=models.CASCADE, related_name='Query')

    def __str__(self):
        return f"{self.search.user} article result for search {self.search.id} ({self.search.search})"
    
    def serialize(self):
        return {
            "id": self.id,
            "headline": self.headline,
            "body": self.body,
            "url": self.url
        }
    
class Likes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='Likes')
    user_liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Person')

    def __str__(self):
        return f"{self.user_liked} liked {self.article.id} with category {self.article.category}"

class Dislikes(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='Disikes')
    user_disliked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Person_d')

    def __str__(self):
        return f"{self.user_liked} disliked {self.article.id} with category {self.article.category}"
