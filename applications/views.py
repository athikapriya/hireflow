from django.shortcuts import render, get_object_or_404, redirect

from .models import Application
from jobs.models import Job
from .forms import ApplicationForm


# =============== apply job view =============== 
def apply_job(request, job_id):
    page_title = "Apply Job"
    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(job=job, candidate=request.user).exists():
        return redirect('applied_jobs')

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.candidate = request.user
            application.save()
            return redirect('applied_jobs')
    else:
        form = ApplicationForm()

    context = {
        "job": job,
        "form": form,
        "page_title": page_title,
    }
    return render(request, "applications/apply_job.html", context)


# =============== Applied jobs =============== 
def applied_jobs(request):
    page_title = "Applied Jobs"

    applications = Application.objects.filter(
        candidate=request.user
    ).select_related('job')

    context = {
        "page_title": page_title,
        "applications": applications,
    }
    return render(request, "applications/applied_jobs.html", context)