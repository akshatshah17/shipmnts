from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Tweet(models.Model):
    tweet_desc = models.CharField(max_length=140)
    tweet_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tweet_desc
