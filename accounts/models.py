# third party imports
from django.contrib.auth.models import AbstractUser
from django.db import models


# =============== User model =============== 
class User(AbstractUser):
    ROLE_CHOICES = (
        ("candidate", "Candidate"),
        ("employer", "Employer"),
    )

    username = models.CharField(max_length=150, unique=True)
    designation = models.CharField(max_length=25, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

    def __str__(self):
        return f'{self.role} - {self.username}'