from django.db import models
from django.conf import settings
from jobs.models import Job  


STATUS_CHOICES = [
    ("pending", "Pending"),
    ("accepted", "Accepted"),
    ("rejected", "Rejected"),
]

# =============== application model =============== 
class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    
    class Meta:
        ordering = ['-applied_at']  
        unique_together = ('job', 'candidate') 

    def __str__(self):
        return f"{self.candidate.username} -> {self.job.title} ({self.status})"