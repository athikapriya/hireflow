from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("browse/", views.browse_jobs, name="browse_jobs"),
    path("manage/", views.manage_jobs, name="manage_jobs"),
    path("create/", views.create_job, name="create_job"),
    path("edit/<int:job_id>/", views.edit_job, name="edit_job"),
    path("delete/<int:job_id>/", views.delete_job, name="delete_job"),
    path("category/<int:category_id>/", views.jobs_by_category, name="jobs_by_category"),
    path("<slug:slug>/", views.job_detail, name="job_detail"), 
]