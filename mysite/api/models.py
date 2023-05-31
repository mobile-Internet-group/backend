from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    is_manager = models.BooleanField(default=0)
    def __str__(self):
        return self.username
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    content_type = models.IntegerField(default=0) #0 or 1
    text = models.CharField(max_length=200)
    media_url = models.CharField(max_length=300)
    location_x = models.FloatField()
    location_y = models.FloatField()
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content_type = models.CharField(max_length=200)
    media_url = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    def __str__(self):
        return self.text