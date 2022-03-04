from django.shortcuts import render

# Create your views here.

def view_basket(request):
    """ Reners the basket template with its contents """
    return render(request, 'basket/basket.html')