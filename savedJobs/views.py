# third party imports
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import candidate_required

# local imports
from .models import SavedJob
from jobs.models import Job


# =============== save job view ===============
@login_required
@candidate_required
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    SavedJob.objects.get_or_create(
        user=request.user,
        job=job
    )

    return redirect("saved_jobs:saved_jobs")



# =============== saved jobs view =============== 
def saved_jobs(request):
    saved_jobs_list = SavedJob.objects.filter(user=request.user).order_by("-saved_at")
    return render(request, "savedJobs/saved_jobs.html", {"saved_jobs": saved_jobs_list})



# =============== unsave jobs view =============== 
def unsave_job(request, job_id):

    saved_job = get_object_or_404(
        SavedJob,
        user=request.user,
        job_id=job_id
    )

    saved_job.delete()

    return redirect("saved_jobs:saved_jobs")