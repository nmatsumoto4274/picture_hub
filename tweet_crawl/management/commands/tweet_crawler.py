import twitter
from django.core.management import BaseCommand

from picture_hub import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        ユーザごとのハッシュタグ付きの画像ツイートを取得し、未登録だったら登録する。
        :param args:
        :param options:
        :return:
        """
        # TODO ツイート取得のバッチを仕込むかアクセスごとに取得するか検討すること。
        # APIインスタンスの作成
        # api = twitter.Api(
        #     consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
        #     consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
        #     access_token_key=user.access_token['oauth_token'],
        #     access_token_secret=user.access_token['oauth_token_secret']
        # )

        print("hogehoge")
