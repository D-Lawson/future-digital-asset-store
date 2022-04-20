from django.shortcuts import render

# Create your views here.


def index(request):
    """ Returns the main index page """
    return render(request, 'home/index.html')
