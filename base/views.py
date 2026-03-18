# third party imports
from django.shortcuts import render



# =============== homepage view =============== 
def homepage(request):
    context={

    }
    return render(request, 'base/homepage.html', context)