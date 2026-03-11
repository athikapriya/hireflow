from django.shortcuts import render, redirect
from .models import JobCompany


# =============== company profile view =============== 
def company_profile(request):
    try:
        company = JobCompany.objects.get(created_by=request.user)
    except JobCompany.DoesNotExist:
        company = None

    context = {"company": company}
    return render(request, "companies/company_profile.html", context)


# =============== edit company view =============== 
def edit_company(request):
    company, created = JobCompany.objects.get_or_create(created_by=request.user)

    if request.method == "POST":
        company.name = request.POST.get("name")
        company.description = request.POST.get("description")
        company.website = request.POST.get("website")
        company.location = request.POST.get("location")
        if request.FILES.get("logo"):
            company.logo = request.FILES.get("logo")
        company.save()
        return redirect("companies:company_profile")

    return render(request, "companies/edit_company.html", {"company": company})