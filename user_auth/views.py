import twitter
from django.shortcuts import render

from social_django.models import UserSocialAuth

from picture_hub import settings


def top_page(request):
    user = None
    if request.user.id is not None:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
    return render(request, 'user_auth/top.html', {'user': user})
