import calendar
import time

import twitter
from django.core.management import BaseCommand
from django.db.models import Max
from social_django.models import UserSocialAuth

from picture_hub import settings
from tweet_crawl.models import Tweet, Picture


class Command(BaseCommand):

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

    """
    ユーザの画像付きツイートを収集するコマンド
    """

    def handle(self, *args, **kwargs):
        # ユーザ情報取得
        users = UserSocialAuth.objects.all()

        for user in users:
            user_id = user.id
            user_uid = user.uid
            token_dict = user.extra_data['access_token']
            api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                              consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                              access_token_key=token_dict['oauth_token'],
                              access_token_secret=token_dict['oauth_token_secret'])
            twitter_user = api.GetUser(user_id=user_uid)

            screen_name = twitter_user.screen_name
            since_id = Tweet.objects.all().aggregate(Max('id'))

            # ツイートの検索
            if since_id is None:
                tweets = api.GetSearch(term='#Pict_Hub -RT filter:images from:' + screen_name)
            else:
                tweets = api.GetSearch(term='#Pict_Hub -RT filter:images from:' + screen_name,
                                       since_id=since_id['id__max'])

            for tweet in tweets:
                if Tweet.objects.filter(id=tweet.id).count() >= 0:
                    t = Tweet(
                        id=tweet.id,
                        user_id=user_id,
                        create_datetime=self.__conv_time(tweet.created_at)
                    )
                    t.save()

                    # 画像の登録
                    for picture in tweet.media:
                        p = Picture(
                            id=picture.id,
                            tweet_id=tweet.id,
                            picture_url=picture.media_url_https
                        )
                        p.save()

            print(twitter_user.screen_name, 'Done!')
