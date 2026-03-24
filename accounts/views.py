from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from .forms import CandidateRegisterForm, EmployerRegisterForm
from jobs.models import Job



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



# =============== employer dashboard view ===============
def employer_dashboard(request):
    page_title = "Dashboard"

    jobs = Job.objects.filter(employer=request.user).order_by('-updated_at')

    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()
    closed_jobs = jobs.filter(is_active=False).count()

    latest_jobs = jobs[:6]

    context = {
        "jobs" : latest_jobs,
        'total_applications': 0,
        # 'shortlisted_candidates': 0,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "closed_jobs" : closed_jobs,
        "page_title" : page_title
    }
    return render(request, 'accounts/employer_dashboard.html', context)


# =============== candidate dashboard view ===============
def candidate_dashboard(request):
    page_title = "Dashboard"

    context = {
        # Example placeholders:
        # 'applied_jobs': 0,
        # 'interviewed_jobs': 0,
        # 'job_offers': 0,
        # 'saved_jobs': 0,
        "page_title" : page_title
    }
    return render(request, 'accounts/candidate_dashboard.html', context)