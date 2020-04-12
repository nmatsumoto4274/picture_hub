import twitter
from django.shortcuts import render

from social_django.models import UserSocialAuth

from picture_hub import settings


def top_page(request):
    user = None
    tweet = None
    if request.user.id is not None:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        # ツイートの取得
        api = twitter.Api(
            consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
            consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
            access_token_key=user.access_token['oauth_token'],
            access_token_secret=user.access_token['oauth_token_secret']
        )
        # RTは除外し、画像付きツイートだけ取得する。
        tweet = api.GetSearch(term='#Pict_Hub -RT filter:images')

    return render(request, 'user_auth/top.html', {'user': user, 'tweet': tweet})


