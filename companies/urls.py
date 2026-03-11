from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
    path("profile/", views.company_profile, name="company_profile"),
    path("edit/", views.edit_company, name="edit_company"),
]