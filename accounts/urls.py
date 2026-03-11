# third party imports
from django.urls import path

# local imports
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile, name="profile"),

    path("candidate/dashboard/", views.candidate_dashboard, name="candidate_dashboard"),
    path("employer/dashboard/", views.employer_dashboard, name="employer_dashboard"),
]