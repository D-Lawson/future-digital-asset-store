from django.shortcuts import render, get_object_or_404
from django.contrib import messages

from .models import UserAccount
from .forms import UserAccountForm

from checkout.models import Order


def account(request):
    """ Show the user's account page. """

    account = get_object_or_404(UserAccount, user=request.user)

    if request.method == 'POST':
        form = UserAccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated details saved to account')
        else:
            messages.error(
                request, 'Please check that the form has been completed \
                    properly.')
    else:
        form = UserAccountForm(instance=account)
    
    orders = account.orders.all()

    template = 'accounts/account.html'
    context = {
        'form': form,
        'orders': orders,
        'viewing_account': True,
    }

    return render(request, template, context)


def previous_orders(request, order_id):
    """ Show the selected previous order. """
    order = get_object_or_404(Order, order_id=order_id)

    messages.info(request, (
        f'Please view the order summary for order {order_id}. '
        'This information was sent to your email on the order date.'
    ))

    template = 'checkout/checkout_completed.html'
    context = {
        'order': order,
        'from_account': True,
    }

    return render(request, template, context)