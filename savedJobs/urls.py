from django.urls import path
from . import views

app_name = "saved_jobs"

urlpatterns = [
    path("", views.saved_jobs, name="saved_jobs"),
    path("save/<int:job_id>/", views.save_job, name="save_job"),
    path("unsave/<int:job_id>/", views.unsave_job, name="unsave_job"),
]