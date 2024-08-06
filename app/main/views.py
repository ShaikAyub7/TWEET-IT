from django.http import FileResponse, Http404
import os
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import timedelta
from .models import Tweet, Story, Profile
from .forms import ProfileForm, ReplyForm, StoryForm, TweetForm, UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.shortcuts import render, redirect
from .models import WhatsNew
from .forms import WhatsNewForm

def base(request):
    return render(request, 'base.html')

def home(request):
    return render(request, 'home.html')

def tweetlist(request,user_id=None):
    if user_id:
        user = get_object_or_404(User, id=user_id)
    else:
        user = request.user if request.user.is_authenticated else None
    
    tweets = Tweet.objects.all().order_by('-created_at')
    search_query = request.GET.get('search',)

    if search_query:
        search_results = Tweet.objects.filter (
            Q(text__icontains = search_query)|
            Q(id__icontains = search_query)|
            Q(photo__icontains = search_query), 
        ).distinct()

        if search_results.exists():
            tweets = search_results
        else:
            messages.error(request, f"No tweets found matching '{search_query}'.")

    active_stories = Story.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).order_by('-created_at')
    # viewed_stories = StoryView.objects.filter(user=user).values_list('story_id', flat=True) if user else []
    context = {
        'tweets': tweets,
        'user': user,
        'search_query': search_query,
        'all_stories': active_stories,
        # 'viewed_stories':viewed_stories,
        'profile_url': reverse('profile', args=[user.id]) if user else '#'
    }
    return render(request, 'tweet_list.html', context)

@login_required
def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        return HttpResponse(f'User profile does not exist. Please create a profile first. \n you can create profile in setting \n 1. go to settings \n 2.select createprofile \n 3.create a profile', status=404)
    tweets = Tweet.objects.filter(user=user).order_by('-created_at')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)  # Ensure user.id is valid
    else:
        form = ProfileForm(instance=profile)
    context = {
        'tweets': tweets,
        'form': form,
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)

@login_required
def tweetcreate(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_detail', tweet_id=tweet.id)
    else:
        form = TweetForm()
    return render(request, 'form.html', {'form': form})

@login_required
def tweetedit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            messages.success(request, 'tweet Edited successfully.')
            return redirect('tweetlist')
    else:
        form = TweetForm(instance=tweet)
    return render(request, 'form.html', {'form': form})

def tweetdelete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)
    if request.method == 'POST':
        tweet.delete()
        messages.success(request, 'tweet deleted successfully.')
        return redirect('tweetlist')
    return render(request, 'delete.html', {'tweet': tweet})

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('tweetlist')
        else:
            messages.error(request, 'user is already taken.')
    return render(request, 'login')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'user is already taken.')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'email is already taken.')
            return redirect('register')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return redirect('login')
    return render(request, 'registration/register.html')


def logout_page(request):
    return redirect('login')
    # return render(request, 'registration/login.html')

@login_required
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    replies = tweet.replies.all()
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.tweet = tweet
            reply.user = request.user
            reply.save()
            return redirect('tweet_detail', tweet_id=tweet.id)
    else:
        form = ReplyForm()
    context = {
        'tweet': tweet,
        'replies': replies,
        'form': form,
    }
    return render(request, 'tweet_detail.html', context)

def reply_create(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.user = request.user
            reply.tweet = tweet
            reply.save()
            return redirect('tweetlist')
    else:
        form = ReplyForm()
    context = {
        'tweet': tweet,
        'form': form,
    }
    return render(request, 'tweet_list.html', context)

# def reply_delete(request, tweet_id, comment_id, reply_id):
#     reply = get_object_or_404(Reply, id=reply_id)

#     if reply.user == request.user:
#         if request.method == 'POST':
#             reply.delete()
#             return redirect('tweet_detail', tweet_id=tweet_id)
#         return render(request, 'delete.html', {'reply': reply})
    
#     return redirect('tweet_detail', tweet_id=tweet_id)

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    user = request.user
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
        return redirect('tweetlist')
    else:
        tweet.likes.add(request.user)
        return redirect('tweetlist')
    return render(request,'tweetlist', tweet_id=tweet.id)

def setting(request):
    return render(request, 'setting.html')

@login_required
def Create_story(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('tweetlist')
    else:
        form = StoryForm()
    return render(request, 'create_story.html', {'form': form})

def search(request):
    query = request.GET.get('q')
    users = User.objects.filter(username__icontains=query) if query else None
    return render(request, 'search.html', {'users': users, 'query': query})

def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile', user_id=request.user.id)
        else:
            messages.error(request, 'There was an error updating your profile. Please try again.')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit-profile.html', {'form': form})

@login_required
def create_profile(request):
    # Check if the user already has a profile
    profile_exists = Profile.objects.filter(user=request.user).exists()
    if profile_exists:
        messages.warning(request, 'You already have a profile.')
        return redirect('tweetlist')  # Redirect to a suitable URL
    
    if request.method == 'POST':
        profile = Profile(user=request.user)
        profile.save()
        messages.success(request, 'Profile created successfully!')
        return redirect('tweetlist')  # Redirect to tweet list or another page after creation
    return render(request, 'create_profile.html')

@login_required
def user_tweets(request):
    tweets = Tweet.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user_tweets.html', {'tweets': tweets})

@login_required
def upload_reel(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.user = request.user
            story.save()
            return redirect('reels')
    else:
        form = StoryForm()
    
    return render(request, 'upload_reel.html', {'form': form})

@login_required
def reels(request):
    reels = Story.objects.filter(video__isnull=False).order_by('-created_at')[:10]  # Fetch latest 10 reels
    return render(request, 'reels.html', {'reels': reels})


def media_view(request, path):
    file_path = os.path.join('/tmp/media', path)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        raise Http404


def whats_new_list(request):
    entries = WhatsNew.objects.all().order_by('-created_at')
    return render(request, 'whats_new_list.html', {'entries': entries})

def add_whats_new(request):
    if request.method == 'POST':
        form = WhatsNewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('whats_new_list')
    else:
        form = WhatsNewForm()
    return render(request, 'add_whats_new.html', {'form': form})

@login_required
def followers(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    if tweet.Follwers.filter(id=request.user.id).exists():
        tweet.Follwers.remove(request.user)
        return redirect('tweetlist')
    else:
        tweet.Follwers.add(request.user)
        return redirect('tweetlist')
    return render(request,'tweetlist', tweet_id=tweet.id)