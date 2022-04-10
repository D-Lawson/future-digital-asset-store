from django.shortcuts import render, get_object_or_404

from .models import UserAccount


def account(request):
    """ Show the user's account page. """

    account_info = get_object_or_404(UserAccount, user=request.user)

    template = 'accounts/account.html'
    context = {
        'account': account_info,
    }

    return render(request, template, context)