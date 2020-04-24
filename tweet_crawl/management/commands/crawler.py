from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    ユーザの画像付きツイートを収集するコマンド
    """

    def handle(self, *args, **kwargs):
        # TODO DBに登録されたユーザの情報を取得し、新たなハッシュタグ・画像付きのツイートが存在するかチェックします。
        print(True)
