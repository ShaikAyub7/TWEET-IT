from django.urls import path
from . import views

urlpatterns = [
    path('', views.tweetlist, name='tweetlist'),
    path('create/', views.tweetcreate, name='tweetcreate'),
    path('tweet/<int:tweet_id>/', views.tweet_detail, name='tweet_detail'),
    path('<int:tweet_id>/edit/', views.tweetedit, name='tweetedit'),
    path('<int:tweet_id>/delete/', views.tweetdelete, name='tweetdelete'),
    # path('<int:tweet_id>/<int:comment_id>/<int:reply_id>/delete/', views.reply_delete, name='reply_delete'),
    path('tweet/<int:tweet_id>/reply/', views.reply_create, name='reply_create'),
    path('accounts/profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('tweet/<int:tweet_id>/like/', views.like_tweet, name='like_tweet'),
    path('setting/', views.setting, name='setting.html'),
    # path('mark-story-viewed/<int:story_id>/', views.mark_story_viewed, name='mark_story_viewed'),
    path('story/', views.Create_story, name='create_story.html'),
    path('search/', views.search, name='search'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('user/', views.user_tweets, name='user'),
    # path('notifications/', views.notifications, name='notifications'),
    # path('notifications/read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('upload/', views.upload_reel, name='upload'),
    path('reels/', views.reels, name='reels'),
    path('api/media/<path:path>', views.media_view),


]
