from django.shortcuts import render
from social_django.models import UserSocialAuth


def top(request):
    """
    トップページのView関数
    TODO ログイン未済の場合はトップページへ遷移し、ログイン済の場合はポートフォリオへリダイレクトします
    :param request: リクエスト
    :return: リソース
    """
    user = None
    if request.user.id is not None:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
    return render(request, 'tweet_crawl/top.html', {'user': user})


def portfolio(request, screen_name):
    """
    ポートフォリオViews
    :param screen_name: Twitter表示名
    :param request: リクエスト
    :return: リソース
    """
    user = None
    # TODO screen_nameがuserテーブルに存在しない場合の処理を検討すること。
    if request.user.id is not None:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
    return render(request, 'tweet_crawl/portfolio.html', {'screen_name': screen_name, 'user': user})
