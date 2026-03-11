# third party imports
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import employer_required
from django.db.models import Q

# local imports
from .models import Job, JobCategory


# List all jobs
def job_list(request):
    jobs = Job.objects.filter(status="active").order_by("-created_at")
    return render(request, "jobs/job_list.html", {"jobs": jobs})


# Job detail view
def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    return render(request, "jobs/job_detail.html", {"job": job})


# Jobs by category
def jobs_by_category(request, category_id):
    category = get_object_or_404(JobCategory, id=category_id)
    jobs = Job.objects.filter(category=category, status="active")
    return render(request, "jobs/jobs_by_category.html", {"jobs": jobs, "category": category})



# =============== browse jobs view =============== 
def browse_jobs(request):

    query = request.GET.get("q")

    jobs = Job.objects.filter(status="active")

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(skills__name__icontains=query)
        ).distinct()

    return render(request, "jobs/browse_jobs.html", {"jobs": jobs})



# =============== create job view =============== 
@login_required
@employer_required
def create_job(request):

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

        Job.objects.create(
            employer=request.user,
            title=title,
            description=description
        )

    return render(request, "jobs/create_job.html")


# =============== edit job view =============== 
@login_required
@employer_required
def edit_job(request, job_id):

    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == "POST":
        job.title = request.POST.get("title")
        job.description = request.POST.get("description")
        job.location = request.POST.get("location")
        job.salary = request.POST.get("salary")
        job.job_type = request.POST.get("job_type")
        job.experience_required = request.POST.get("experience_required")
        job.save()

        return redirect("jobs:manage_jobs")

    return render(request, "jobs/edit_job.html", {"job": job})




# =============== delete job view =============== 
@login_required
@employer_required
def delete_job(request, job_id):

    job = get_object_or_404(Job, id=job_id, employer=request.user)

    if request.method == "POST":
        job.delete()
        return redirect("jobs:manage_jobs")

    return render(request, "jobs/delete_job.html", {"job": job})



# =============== manage job view =============== 
@login_required
@employer_required
def manage_jobs(request):

    jobs = Job.objects.filter(employer=request.user)

    return render(request, "jobs/manage_jobs.html", {"jobs": jobs})