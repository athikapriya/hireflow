# third party imports
from django.shortcuts import render



# =============== homepage view starts =============== 

def homepage(request):
    context = {}
    return render(request, 'base/homepage.html', context)

# =============== homepage view ends =============== 