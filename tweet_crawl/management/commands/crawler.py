import twitter
from django.db.models import Max
from social_django.models import UserSocialAuth
from django.core.management import BaseCommand

from picture_hub import settings
from tweet_crawl.models import Tweet


class Command(BaseCommand):
    """
    ユーザの画像付きツイートを収集するコマンド
    """

    def handle(self, *args, **kwargs):
        # ユーザ情報取得
        users = UserSocialAuth.objects.all()

        for user in users:
            uid = user.uid
            token_dict = user.extra_data['access_token']
            api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                              consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                              access_token_key=token_dict['oauth_token'],
                              access_token_secret=token_dict['oauth_token_secret'])
            twitter_user = api.GetUser(user_id=uid)

            screen_name = twitter_user.screen_name
            since_id = Tweet.objects.all().aggregate(Max('id'))

            # ツイートの検索
            if since_id is None:
                tweets = api.GetSearch(term='#Pict_Hub -RT filter:images from:' + screen_name)
            else:
                tweets = api.GetSearch(term='#Pict_Hub -RT filter:images from:' + screen_name,
                                       since_id=since_id['id__max'])

            # 登録未済のツイートが存在していたら、取得して登録
            for tweet in tweets:
                print(twitter_user.screen_name, since_id, tweets)
