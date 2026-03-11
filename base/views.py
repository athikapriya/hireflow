# third party imports
from django.shortcuts import render
from .models import *



# =============== employer dashboard view starts =============== 
def homepage(request):
    context = {}
    return render(request, "base/homepage.html", context)

# =============== employer dashboard view ends =============== 