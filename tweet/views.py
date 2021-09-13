from django.shortcuts import render, redirect
from django.contrib import messages
from tweet.models import Tweet
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/accounts/login")
def add(request):
    if request.method == 'POST':
        tweet = request.POST['tweet']
        if len(tweet) <= 140:
            obj = Tweet(tweet_desc=tweet, tweet_owner_id=request.user.id)
            obj.save()
            return redirect('/accounts/profile')
        else:
            messages.error(request, 'Tweet size must be less than or equal to 140 characters.')
            return redirect('/accounts/profile')
    else:
        return redirect('/accounts/profile')
