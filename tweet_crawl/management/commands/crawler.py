import calendar
import time

import twitter
from django.core.management import BaseCommand
from django.db.models import Max
from social_django.models import UserSocialAuth

from picture_hub import settings
from tweet_crawl.models import Tweet, Picture


class Command(BaseCommand):
    """
    ユーザの画像付きツイートを収集するコマンド
    """

    def __conv_time(self, created_at):
        """
        Twitter のcreated_at をDATETIMEで扱える形に変換する。
        :param created_at:
        :return:
        """
        time_utc = time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        unix_time = calendar.timegm(time_utc)
        time_local = time.localtime(unix_time)
        japan_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return japan_time

    def __get_tweets(self, api, uid, since_id):
        """
        ツイートの取得
        :param api: Twitter APIのインスタンス
        :param uid: Twitterのuid
        :param since_id: Tweetテーブルに存在するレコードのID最大値
        :return: Tweetリスト
        """
        result = []
        if since_id:
            tweets = api.GetUserTimeline(user_id=uid, since_id=since_id['id__max'], count=200, include_rts=False)
        else:
            tweets = api.GetUserTimeline(user_id=uid, count=200, include_rts=False)
        for tweet in tweets:
            if tweet.media is not None and len(tweet.hashtags) > 0:
                tags = []
                for t in tweet.hashtags:
                    tags.append(t.text)
                if "Pict_Hub" in tags:
                    result.append(tweet)
                    break
        return result

    def handle(self, *args, **kwargs):
        """
        メイン関数
        :param args:
        :param kwargs:
        :return:
        """
        users = UserSocialAuth.objects.all()
        for user in users:
            token_dict = user.extra_data['access_token']
            api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                              consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                              access_token_key=token_dict['oauth_token'],
                              access_token_secret=token_dict['oauth_token_secret'])
            tweets = self.__get_tweets(api, user.uid, Tweet.objects.all().aggregate(Max('id')))
            for tweet in tweets:
                if Tweet.objects.filter(id=tweet.id).count() >= 0:
                    t = Tweet(id=tweet.id, user_id=user.id, create_datetime=self.__conv_time(tweet.created_at))
                    t.save()
                    for picture in tweet.media:
                        p = Picture(id=picture.id, tweet_id=tweet.id, picture_url=picture.media_url_https)
                        p.save()
            print(user.uid, 'Done!')
        print('All tasks Done!')
