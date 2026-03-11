from django.shortcuts import redirect


def employer_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.role != "Employer":
            return redirect("homepage")

        return view_func(request, *args, **kwargs)

    return wrapper


def candidate_required(view_func):

    def wrapper(request, *args, **kwargs):

        if request.user.role != "Candidate":
            return redirect("homepage")

        return view_func(request, *args, **kwargs)

    return wrapper