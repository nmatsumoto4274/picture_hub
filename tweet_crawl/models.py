from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    """
    ツイート
    """
    id = models.BigIntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_datetime = models.DateTimeField()


class Picture(models.Model):
    """
    写真
    """
    id = models.BigIntegerField(primary_key=True)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    picture_url = models.URLField(max_length=200)
