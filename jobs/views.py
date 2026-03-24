from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Job, Skill
from .forms import JobForm
from applications.models import Application
from accounts.decorators import candidate_required, employer_required


# =============== manage Jobs view =============== 
@login_required(login_url="login")
@employer_required
def manage_jobs(request):
    page_title = "Manage Jobs"
    today = timezone.now().date()

    Job.objects.filter(deadline__lt=today, is_active=True).update(is_active=False)

    query = request.GET.get("q", "")
    employment_type = request.GET.get("employment_type", "")
    status = request.GET.get("status", "")

    jobs = Job.objects.all().order_by("-is_active", "-posted_at")

    if query:
        jobs = jobs.filter(title__icontains=query)

    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)

    if status:
        if status == "active":
            jobs = jobs.filter(is_active=True)
        elif status == "closed":
            jobs = jobs.filter(is_active=False)

    total_jobs_filtered = jobs.count()
    total_jobs_all = Job.objects.count()

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get("page")
    jobs_page = paginator.get_page(page_number)

    context = {
        "page_title": page_title,
        "jobs": jobs_page,
        "query": query,
        "employment_type": employment_type,
        "status": status,
        "total_jobs_filtered": total_jobs_filtered,
        "total_jobs_all": total_jobs_all,
        "today": today,
    }
    return render(request, "jobs/manage_jobs.html", context)



# =============== create job view =============== 
@login_required(login_url="login")
@employer_required
def create_job(request):
    page_title = "Create Job"

    if request.method == "POST":
        form = JobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()

            skills_str = form.cleaned_data["skills"]
            if skills_str:
                skill_names = [s.strip() for s in skills_str.split(",") if s.strip()]
                for name in skill_names:
                    skill_obj, created = Skill.objects.get_or_create(name=name)
                    job.skills.add(skill_obj)

            return redirect("manage_jobs")  
    else:
        form = JobForm()
    
    context = {
        "form": form,
        "page_title" : page_title
        }
    return render(request, "jobs/job_form.html", context)


# =============== Edit Job ===============
@login_required(login_url="login")
@employer_required
def edit_job(request, pk):
    page_title = "Edit Job"

    job = get_object_or_404(Job, id=pk, employer=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            job = form.save(commit=False)
            job.save()

            job.skills.clear()

            skills_str = form.cleaned_data.get("skills", "")
            if skills_str:
                skill_names = [s.strip() for s in skills_str.split(",") if s.strip()]
                for name in skill_names:
                    skill_obj, _ = Skill.objects.get_or_create(name=name)
                    job.skills.add(skill_obj)

            return redirect("manage_jobs")
    else:
        initial_skills = ", ".join(job.skills.values_list("name", flat=True))
        form = JobForm(instance=job, initial={"skills": initial_skills})

    context = {
        "form": form,
        "job": job,
        "page_title": page_title,
    }
    return render(request, "jobs/job_form.html", context)


# =============== Delete Job ===============
@login_required(login_url="login")
@employer_required
def delete_job(request, pk):
    job = get_object_or_404(Job, id=pk, employer=request.user)

    job.is_active = False
    job.save()

    return redirect("manage_jobs")


# =============== Restore Job ===============
@login_required(login_url="login")
@employer_required
def restore_job(request, pk):
    job = get_object_or_404(Job, id=pk, employer=request.user)

    job.is_active = True
    job.save()

    return redirect("manage_jobs")



# =============== browse jobs view =============== 
@login_required(login_url="login")
@candidate_required
def browse_jobs(request):
    page_title = "Browse Jobs"

    jobs = Job.objects.all().order_by('-is_active', '-updated_at')

    query = request.GET.get('q', '')                
    employment_type = request.GET.get('employment_type', '')  
    status = request.GET.get('status', '')          

    if query:
        jobs = jobs.filter(title__icontains=query)

    if employment_type:
        jobs = jobs.filter(employment_type=employment_type)

    if status:
        if status == "active":
            jobs = jobs.filter(is_active=True)
        elif status == "closed":
            jobs = jobs.filter(is_active=False)

    if request.user.is_authenticated:
        applied_job_ids = list(
            request.user.applications.values_list('job_id', flat=True)
        )

    total_jobs_filtered = jobs.count()
    total_jobs_all = Job.objects.count()

    paginator = Paginator(jobs, 6)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)

    context = {
        "page_title" : page_title,
        "jobs": jobs_page, 
        "query": query,
        "employment_type": employment_type,
        "status": status,
        "total_jobs_filtered": total_jobs_filtered,
        "total_jobs_all": total_jobs_all,
        "applied_job_ids": applied_job_ids,
    }
    return render(request, 'jobs/browse_jobs.html', context)



# =============== job overview view =============== 
@login_required(login_url="login")
@candidate_required
def job_details(request, pk):
    job = get_object_or_404(Job, id=pk)

    has_applied = False

    if request.user.is_authenticated:
        has_applied = Application.objects.filter(
            job=job,
            candidate=request.user
        ).exists()

    context = {
        "job": job,
        "has_applied": has_applied,
    }
    return render(request, 'jobs/job_details.html', context)