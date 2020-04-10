from django.contrib.auth.models import User
from django.db import models


class Picture(models.Model):
    """
    写真
    """
    tweet_id = models.IntegerField(primary_key=True)
    picture_url = models.URLField(max_length=200)


class Tweet(models.Model):
    """
    ツイート
    """
    pictures = models.ForeignKey(Picture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_datetime = models.DateField()
