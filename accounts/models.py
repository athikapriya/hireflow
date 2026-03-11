from django.db import models
from django.contrib.auth.models import AbstractUser


# =============== user model =============== 
class User(AbstractUser):
    ROLE_CHOICES = (
        ("Employer", "Employer"),
        ("Candidate", "Candidate"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username



# =============== candidate profile =============== 
class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)

    skills = models.ManyToManyField("jobs.Skill", blank=True)

    experience = models.TextField(blank=True)
    resume = models.FileField(upload_to='candidate_resumes/', blank=True, null=True)

    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)

    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username
    


# =============== employer profile =============== 
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    designation = models.CharField(max_length=200)

    company = models.ForeignKey(
        "companies.JobCompany",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.user.username