from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Application
from jobs.models import Job
from .forms import ApplicationForm
from accounts.decorators import candidate_required, employer_required


# =============== apply job view =============== 
@login_required(login_url="login")
@candidate_required
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
@login_required(login_url="login")
@candidate_required
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



# =============== employer applications view =============== 
@login_required(login_url="login")
@employer_required
def employer_applications(request):
    page_title = "Applications"

    jobs = Job.objects.filter(employer=request.user) 
    applications_list = Application.objects.filter(job__in=jobs).select_related('job', 'candidate')

    paginator = Paginator(applications_list, 10)
    page_number = request.GET.get('page')
    applications = paginator.get_page(page_number)

    context = {
        'applications': applications,
        'page_title': page_title
    }
    return render(request, 'applications/employer_applications.html', context)


# =============== accept application view =============== 
@login_required(login_url="login")
@employer_required
def accept_application(request, app_id):
    application = get_object_or_404(Application, id=app_id, job__employer=request.user)
    application.status = "accepted"
    application.save()
    return redirect('employer_applications')


# =============== reject application view =============== 
@login_required(login_url="login")
@employer_required
def reject_application(request, app_id):
    application = get_object_or_404(Application, id=app_id, job__employer=request.user)
    application.status = "rejected"
    application.save()
    return redirect('employer_applications')