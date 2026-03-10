# third party imports
from django.urls import path


# local imports
from .import views


# =============== urlpatterns =============== 
urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
]
