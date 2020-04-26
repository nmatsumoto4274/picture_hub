from django.shortcuts import render
from social_django.models import UserSocialAuth

from tweet_crawl.models import Tweet


def top(request):
    """
    トップページのView関数
    :param request: リクエスト
    :return: リソース
    """
    user = None
    if request.user.id is not None:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
    return render(request, 'tweet_crawl/top.html', {'user': user})


def portfolio(request, screen_name):
    """
    ポートフォリオページのView関数
    TODO ポートフォリオ移動前に、対象ツイートの件数を取得し、DBに登録されている件数より多ければ、update画面へ遷移
    :param screen_name: Twitter表示名
    :param request: リクエスト
    :return: リソース
    """
    user = None
    if request.user.id is not None:
        user = UserSocialAuth.objects.get(user_id=request.user.id)

    # レコード取得
    tweet_list = Tweet.objects.filter(user_id__username=screen_name)

    return render(request, 'tweet_crawl/portfolio.html',
                  {'screen_name': screen_name, 'user': user, 'tweet_list': tweet_list})
