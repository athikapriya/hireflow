# third party imports
from django.shortcuts import render



# =============== homepage view starts =============== 

def dashboard(request):
    context = {}
    return render(request, 'base/dashboard.html', context)

# =============== homepage view ends =============== 