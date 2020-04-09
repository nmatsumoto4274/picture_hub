from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from social_django.models import UserSocialAuth


def top_page(request):
    user = None
    if request.user.id is not None:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
    return render(request, 'user_auth/top.html', {'user': user})
