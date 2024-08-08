from django.db import models
# Create your models here.
from django.db import models
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
import pytz
from django.contrib.auth.models import User
from django_countries.fields import CountryField



# Create your models here.

# class User(User):
#     phone_number= models.IntegerField(max_length=10)
    
class Tweet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=240)
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)  # Add this line
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='liked_tweets', blank=True)
    Follwers = models.ManyToManyField(User,related_name='follwers',blank=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.text[:10]}'
        
    def total_likes(self):
        return self.likes.count()
    

    def created_at_in_user_timezone(self):
        user_timezone = pytz.timezone(self.user.profile.timezone)
        return self.created_at.astimezone(user_timezone)

class Profile(models.Model): 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    timezone = models.CharField(max_length=100, default='Asia/Kolkata')  # Default to India's timezone
    country = CountryField(blank=True, null=True)  # Add this line
    def __str__(self):
        return self.user.username

class Reply(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=240)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
    
    def created_at_in_user_timezone(self):
        user_timezone = pytz.timezone(self.user.profile.timezone)
        return self.created_at.astimezone(user_timezone)

class Story(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stories',null=True, blank=True)
    video = models.FileField(upload_to='videos/', null=True, blank=True)  # Add this line
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

    def is_active(self):
        return timezone.now() < self.created_at + timedelta(hours=24)
    
    def created_at_in_user_timezone(self):
        user_timezone = pytz.timezone(self.user.profile.timezone)
        return self.created_at.astimezone(user_timezone)
# class StoryView(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     story = models.ForeignKey(Story, on_delete=models.CASCADE)
#     viewed_at = models.DateTimeField(auto_now_add=True)

from django.db import models

class WhatsNew(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='news',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
