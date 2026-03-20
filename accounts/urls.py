from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomSetPasswordForm



urlpatterns = [
    # =============== register urls =============== 
    path('register/candidate/', views.candidate_register, name="candidate_register"),
    path("register/employer/", views.employer_register, name="employer_register"),

    # =============== login and logout urls =============== 
    path('login/', views.login_user, name='login'),
    path("logout/", views.logout_user, name="logout"),

    # =============== Password reset urls ===============
    path("register/password_reset/", 
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), 
        name="password_reset"),

    path("register/password_reset/done/", 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_done"),

    path("registration/reset/<uidb64>/<token>/", 
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html", form_class=CustomSetPasswordForm), 
         name="password_reset_confirm"),
         
    path("registration/reset/done/", 
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), 
         name="password_reset_complete"),

    # =============== dashboards =============== 
    path('candidate/dashboard/', views.candidate_dashboard, name="candidate_dashboard"),
    path("employer/dashboard/", views.employer_dashboard, name="employer_dashboard"),
]
