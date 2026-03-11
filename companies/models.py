from django.db import models
from accounts.models import User


# =============== job company =============== 
class JobCompany(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    website = models.URLField(blank=True)

    logo = models.ImageField(upload_to="company_logos/", null=True, blank=True)

    location = models.CharField(max_length=200)

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="companies"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name