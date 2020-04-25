import twitter
from social_django.models import UserSocialAuth
from django.core.management import BaseCommand

from picture_hub import settings


class Command(BaseCommand):
    """
    ユーザの画像付きツイートを収集するコマンド
    """

    def handle(self, *args, **kwargs):
        # TODO DBに登録されたユーザの情報を取得し、新たなハッシュタグ・画像付きのツイートが存在するかチェックします。
        # ユーザ情報取得
        users = UserSocialAuth.objects.all()

        for user in users:
            # 必要なユーザ情報を取り出し
            uid = user.uid
            token_dict = user.extra_data['access_token']

            api = twitter.Api(consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
                              consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
                              access_token_key=token_dict['oauth_token'],
                              access_token_secret=token_dict['oauth_token_secret'])

            # uidに紐づくユーザ情報取得
            twitter_user = api.GetUser(user_id=uid)
            screen_name = twitter_user.screen_names

            # 検索に必要なツイート情報を取得

            # 登録未済のツイートが存在していたら、取得して登録

            print(twitter_user.screen_name)
