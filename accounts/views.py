from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count


from .forms import CandidateRegisterForm, EmployerRegisterForm, CandidateProfileForm, EmployerProfileForm
from applications.models import Application
from jobs.models import Job
from .decorators import candidate_required, employer_required


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
@login_required(login_url="login")
@employer_required
def employer_dashboard(request):
    page_title = "Dashboard"

    jobs = Job.objects.filter(employer=request.user) \
        .annotate(application_count=Count('applications')) \
        .order_by('-updated_at')

    total_jobs = jobs.count()
    active_jobs = jobs.filter(is_active=True).count()
    closed_jobs = jobs.filter(is_active=False).count()

    latest_jobs = jobs[:6]

    total_applications = Application.objects.filter(job__in=jobs).count()

    total_hired = Application.objects.filter(
        job__in=jobs,
        status="accepted"
    ).values('job').distinct().count()

    context = {
        "jobs": latest_jobs,
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "closed_jobs": closed_jobs,
        "total_applications": total_applications,
        "total_hired": total_hired,
        "page_title": page_title,
    }

    return render(request, 'accounts/employer_dashboard.html', context)


# =============== candidate dashboard view ===============
@login_required(login_url="login")
@candidate_required
def candidate_dashboard(request):
    page_title = "Dashboard"

    total_applied = Application.objects.filter(candidate=request.user).count()
    total_accepted = Application.objects.filter(candidate=request.user, status="accepted").count()
    total_pending = Application.objects.filter(candidate=request.user, status="pending").count()
    total_rejected = Application.objects.filter(candidate=request.user, status="rejected").count()

    recent_applications = Application.objects.filter(candidate=request.user)\
                            .select_related('job', 'job__employer')\
                            .order_by('-applied_at')[:6]

    context = {
        "page_title": page_title,
        "total_applied": total_applied,
        "total_accepted": total_accepted,
        "total_pending": total_pending,
        "total_rejected": total_rejected,
        "recent_applications": recent_applications,
    }

    return render(request, 'accounts/candidate_dashboard.html', context)


# =============== profile view =============== 
@login_required(login_url="login")
def profile_view(request):
    user = request.user
    page_title = "My Profile"

    context = {
        "page_title": page_title,
        "user": user,
    }
    return render(request, 'accounts/profile_view.html', context)


# =============== employer profile settings view =============== 
@login_required(login_url="login")
@employer_required
def employer_profileSettings(request):
    page_title = "Profile Settings"

    if request.method == "POST":
        form = EmployerProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = EmployerProfileForm(instance=request.user)

    context = {
        "page_title": page_title,
        "form": form,
    }
    return render(request, 'accounts/profile_form.html', context)



# =============== candidate profile settings view =============== 
@login_required(login_url="login")
@candidate_required
def candidate_profileSettings(request):
    page_title = "Profile Settings"

    if request.method == "POST":
        form = CandidateProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = CandidateProfileForm(instance=request.user)

    context = {
        "page_title": page_title,
        "form": form,
    }
    return render(request, 'accounts/profile_form.html', context)