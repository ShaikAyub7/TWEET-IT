from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        fields = ['text', 'photo','video']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic','country']

# forms.py
from django import forms
from .models import Reply

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add a comment...'}),
        }

from .models import Story

class StoryForm(forms.ModelForm):
    class Meta:
        model = Story
        fields = ['video','image']