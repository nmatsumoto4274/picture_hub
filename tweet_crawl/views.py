from django.shortcuts import render
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth

from tweet_crawl.models import Tweet, Picture


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
    :param screen_name: Twitter表示名
    :param request: リクエスト
    :return: リソース
    """
    user = None
    if request.user.id is not None:
        user = UserSocialAuth.objects.get(user_id=request.user.id)

    # screen_nameからuser情報取得
    user_id = User.objects.values_list('id', flat=True).filter(username=screen_name)

    # レコード取得
    picture_list = Picture.objects.filter(tweet__user_id=user_id[0])

    return render(request, 'tweet_crawl/portfolio.html',
                  {'screen_name': screen_name, 'user': user, 'picture_list': picture_list})
