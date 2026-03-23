from django.urls import path

from .import views

urlpatterns = [
    path("manage_jobs/", views.manage_jobs, name="manage_jobs"),
    path("manage_jobs/create_job/", views.create_job, name="create_job"),
    path("manage_jobs/edit_job/<int:pk>/", views.edit_job, name="edit_job"),
    path("manage_jobs/delete_job/<int:pk>/", views.delete_job, name="delete_job"),
    path("manage_jobs/restore_job/<int:pk>/", views.restore_job, name="restore_job"),
]