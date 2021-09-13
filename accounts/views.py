from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.utils import formats
from tweet.models import Tweet
from accounts.models import UserFollowing


# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    auth.login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register_user.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required(login_url="/accounts/login")
def logout(request):
    auth.logout(request)
    return redirect('/')


class tweet_object:
    def __init__(self, tweet_created, tweet_desc):
        self.tweet_created = tweet_created
        self.tweet_desc = tweet_desc


@login_required(login_url="/accounts/login")
def profile(request):
    user = request.user
    user.date_joined = formats.date_format(user.date_joined, "M d, Y")
    temp = Tweet.objects.all().values_list('tweet_desc', 'tweet_owner', 'tweet_created')
    followers = len(UserFollowing.objects.filter(user_id=user.id).values('id', 'following_user_id'))
    following = len(UserFollowing.objects.filter(following_user_id=user.id).values('id', 'user_id'))
    tweet = list()
    for val in temp:
        tp = list(val)
        if tp[1] == user.id:
            tweet.append(tweet_object(tp[2], tp[0]))
    tweet.reverse()
    length = len(tweet)
    return render(request, "profile.html", {'user': user, 'tweet': tweet, 'length': length, 'following': following,
                                            'followers': followers})


@login_required(login_url="/accounts/login")
def user(request, username):
    if request.user.username != username:
        user_search = User.objects.filter(username=username).values('id', 'username', 'first_name', 'last_name')
        user_search = user_search[0]
        temp = Tweet.objects.all().values_list('tweet_desc', 'tweet_owner', 'tweet_created')
        followers = len(UserFollowing.objects.filter(user_id=user_search['id']).values('id', 'following_user_id'))
        following = len(UserFollowing.objects.filter(following_user_id=user_search['id']).values('id', 'user_id'))
        values = UserFollowing.objects.filter(user_id=user_search['id']).values('following_user_id')
        boolean = False
        for val in values:
            if val['following_user_id'] == request.user.id:
                boolean = True
        tweet = list()
        for val in temp:
            tp = list(val)
            if tp[1] == user_search['id']:
                tweet.append(tweet_object(tp[2], tp[0]))
        length = len(tweet)
        tweet.reverse()
        return render(request, 'user.html', {'user': user_search, 'tweet': tweet, 'length': length,
                                             'following': following, 'followers': followers, 'boolean': boolean})
    else:
        return redirect('/search')


@login_required(login_url="/accounts/login")
def follow(request, user_id):
    if User.objects.filter(id=user_id):
        follow_user = User.objects.filter(id=user_id).values('username')
        follow_user = follow_user[0]['username']
        link = '/accounts/user/' + follow_user
        temp = User.objects.all()
        follow_user_object = None
        for t in temp:
            if t.id == user_id:
                follow_user_object = t
                break
        followed = UserFollowing.objects.filter(user_id=user_id).values('following_user_id')
        for follower in followed:
            if follower['following_user_id'] == request.user.id:
                return redirect(link)
        obj = UserFollowing(user_id=follow_user_object, following_user_id=request.user)
        obj.save()
        return redirect(link)
    else:
        return redirect('/')


@login_required(login_url="/accounts/login")
def unfollow(request, user_id):
    if User.objects.filter(id=user_id):
        unfollow_user = User.objects.filter(id=user_id).values('username')
        unfollow_user = unfollow_user[0]['username']
        link = '/accounts/user/' + unfollow_user
        temp = User.objects.all()
        unfollow_user_object = None
        for t in temp:
            if t.id == user_id:
                unfollow_user_object = t
                break
        obj = UserFollowing.objects.filter(user_id=unfollow_user_object.id, following_user_id=request.user.id)
        obj.delete()
        return redirect(link)
    else:
        return redirect('/')
