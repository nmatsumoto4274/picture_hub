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

    def __get_tweets(self, api, screen_name, since_id):
        """
        ツイートの取得
        :param api: Twitter APIのインスタンス
        :param screen_name: Twitter表示名
        :param since_id: Tweetテーブルに存在するレコードのID最大値
        :return: Tweetリスト
        """
        term = '#Pict_Hub -RT filter:images from:' + screen_name
        return api.GetSearch(term=term) if since_id is None else api.GetSearch(term=term, since_id=since_id['id__max'])

    def handle(self, *args, **kwargs):
        users = UserSocialAuth.objects.all()
        for user in users:
            # TODO ユーザの件数分だけ検索APIを実行しているが、この状態だとAPI限界達してしまうため、ユーザタイムライン取得に変更する
            # Twitter APIインスタンスの生成
            token_dict = user.extra_data['access_token']
            api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                              consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                              access_token_key=token_dict['oauth_token'],
                              access_token_secret=token_dict['oauth_token_secret'])

            # Twitter APIで取得した最新のユーザ情報を正として利用する
            twitter_user = api.GetUser(user_id=user.uid)

            # 未登録ツイートの検索・取得
            tweets = self.__get_tweets(api, twitter_user.screen_name, Tweet.objects.all().aggregate(Max('id')))

            # 登録処理
            for tweet in tweets:
                if Tweet.objects.filter(id=tweet.id).count() >= 0:
                    t = Tweet(id=tweet.id, user_id=user.id, create_datetime=self.__conv_time(tweet.created_at))
                    t.save()
                    for picture in tweet.media:
                        p = Picture(id=picture.id, tweet_id=tweet.id, picture_url=picture.media_url_https)
                        p.save()

            print(twitter_user.screen_name, 'Done!')
        print('All tasks Done!')
