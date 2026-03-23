from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Job, Skill
from .forms import JobForm


# =============== manage Jobs view =============== 
def manage_jobs(request):
    page_title = "Manage Jobs"

    today = timezone.now().date()

    Job.objects.filter(deadline__lt=today, is_active=True).update(is_active=False)

    jobs = Job.objects.all().order_by('-is_active', '-posted_at')

    context = {
        "page_title" : page_title,
        "jobs": jobs,
        "today": today
    }
    return render(request, 'jobs/manage_jobs.html', context)



# =============== create job view =============== 
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
def delete_job(request, pk):
    job = get_object_or_404(Job, id=pk, employer=request.user)

    job.is_active = False
    job.save()

    return redirect("manage_jobs")


# =============== Restore Job ===============
def restore_job(request, pk):
    job = get_object_or_404(Job, id=pk, employer=request.user)

    job.is_active = True
    job.save()

    return redirect("manage_jobs")