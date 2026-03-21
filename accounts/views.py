# third pary imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# local imports
from .forms import CandidateRegisterForm, EmployerRegisterForm


# =============== candidate register view =============== 
def candidate_register(request):

    form = CandidateRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.role = "candidate"
        user.save()
        login(request, user)
        return redirect("login")
    
    context = {
        "form" : form
    }

    return render(request, "accounts/register.html", context)


# =============== employer register view =============== 
def employer_register(request):

    form = EmployerRegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.role = "employer"
        user.save()
        login(request, user)
        return redirect("login")
    
    context = {
        "form" : form
    }

    return render(request, "accounts/register.html", context)



# =============== login view =============== 
def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.role == "employer":
                return redirect("employer_dashboard")
            else:
                return redirect("candidate_dashboard")
        else:
            messages.error(request, "Invalid username or password")

    context = {

    }
    return render(request, 'accounts/login.html', context)



# =============== logout view =============== 
def logout_user(request):
    logout(request)
    return redirect("login")



# =============== candidate dashboard view =============== 
def candidate_dashboard(request):
    context = {
        # applied_jobs
        # interviewed_jobs
        # job_offers
        # saved_jobs
    }
    return render(request, 'accounts/candidate_dashboard.html', context)



# =============== employer dashboard view =============== 
def employer_dashboard(request):
    context = {
        # total_jobs
        # total_applications
        # active_jobs
        # shortlisted_candidates
    }
    return render(request, 'accounts/employer_dashboard.html', context)