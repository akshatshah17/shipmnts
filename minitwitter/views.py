from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from accounts.models import UserFollowing
from tweet.models import Tweet


# Create your views here.
class tweet_object:
    def __init__(self, username, tweet_desc, tweet_created):
        self.username = username
        self.tweet_desc = tweet_desc
        self.tweet_created = tweet_created


def index(request):
    user = UserFollowing.objects.filter(following_user_id=request.user.id).values('user_id')
    tweets = list()
    for val in user:
        extract_tweet = Tweet.objects.filter(tweet_owner=val['user_id']).values('tweet_desc', 'tweet_created')
        extract_username = User.objects.filter(id=val['user_id']).values('username')
        extract_username = extract_username[0]
        for tweet in extract_tweet:
            tweets.append(tweet_object(extract_username['username'], tweet['tweet_desc'], tweet['tweet_created']))
    length = len(tweets)
    tweets.sort(key=lambda x: x.tweet_created, reverse=True)
    return render(request, "index.html", {'tweets': tweets, 'length': length})


@login_required(login_url="/accounts/login")
def search(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists() and request.user.username != username:
            link = '/accounts/user/' + username
            return redirect(link)
        else:
            messages.error(request, 'No User Found.')
            return redirect('/search')
    else:
        return render(request, 'search.html')
