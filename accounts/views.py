# third party imports
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from jobs.models import Job
from applications.models import Application
from savedJobs.models import SavedJob
from .models import CandidateProfile, EmployerProfile

# local imports
from .models import User


# =============== register view =============== 
from .models import CandidateProfile, EmployerProfile

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            role=role
        )

        # Create profile based on role
        if role == "Candidate":
            CandidateProfile.objects.get_or_create(user=user)

        if role == "Employer":
            EmployerProfile.objects.get_or_create(user=user)

        messages.success(request, "Account created successfully!")
        return redirect("login")

    return render(request, "accounts/register.html")



# =============== login view =============== 
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.role == "Employer":
                return redirect("employer_dashboard")

            elif user.role == "Candidate":
                return redirect("candidate_dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")



# =============== logout view =============== 

def logout_view(request):
    logout(request)
    return redirect('login')



# =============== profile view =============== 
def profile(request):
    return render(request, "accounts/profile.html")



# =============== candidate dashboard view =============== 
@login_required
def candidate_dashboard(request):
    # Ensure candidate profile exists, create if not
    candidate_profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
    
    # Use correct field names
    applications = Application.objects.filter(candidate=request.user)  # 'candidate' field
    saved_jobs = SavedJob.objects.filter(user=request.user)          # 'user' field
    
    jobs = Job.objects.filter(status="active")
    
    context = {
        "candidate": candidate_profile,
        "applications": applications,
        "saved_jobs": saved_jobs,
        "jobs": jobs,
    }
    
    return render(request, "accounts/candidate_dashboard.html", context)



# =============== employer dashboard =============== 
def employer_dashboard(request):
    try:
        employer_profile = EmployerProfile.objects.get(user=request.user)
    except EmployerProfile.DoesNotExist:
        # Create one automatically if missing
        employer_profile = EmployerProfile.objects.create(user=request.user)

    # Jobs posted by employer
    jobs = Job.objects.filter(employer=request.user)

    # Applications received
    applications = Application.objects.filter(job__employer=request.user)

    # Company info
    company = employer_profile.company

    context = {
        "employer": employer_profile,
        "jobs": jobs,
        "applications": applications,
        "company": company,
    }

    return render(request, "accounts/employer_dashboard.html", context)