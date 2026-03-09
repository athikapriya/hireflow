# third party imports
from django.db import models
from django.contrib.auth.models import AbstractUser


# =============== User Model =============== 
class User(AbstractUser):
    ROLE_CHOICES = (
        ("Employer", "Employer"),
        ("Candidate", 'Candidate'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to="profiles/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username



# =============== company model =============== 
class JobCompany(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)

    location = models.CharField(max_length=200)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name