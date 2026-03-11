# third party imports
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from accounts.decorators import candidate_required

# local imports
from .models import Application
from jobs.models import Job


# =============== apply job view ===============
@login_required
@candidate_required
def apply_job(request, job_id):

    job = Job.objects.get(id=job_id)

    Application.objects.create(
        candidate=request.user,
        job=job
    )

    return redirect("applied_jobs")


# =============== applied jobs view =============== 
def applied_jobs(request):
    applications = Application.objects.filter(candidate=request.user)
    return render(request, "applications/applied_jobs.html", {"applications": applications})


# =============== job applications view =============== 
def job_applications(request, job_id):
    applications = Application.objects.filter(job_id=job_id)
    return render(request, "applications/job_applications.html", {"applications": applications})