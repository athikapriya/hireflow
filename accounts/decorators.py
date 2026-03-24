from django.shortcuts import redirect
from functools import wraps

def candidate_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'candidate':
            return view_func(request, *args, **kwargs)
        return redirect('login') 
    return wrapper


def employer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'employer':
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper