from django.db import models
from django.core.exceptions import ValidationError



# =============== validate resume =============== 
def validate_resume(file):

    allowed_extensions = ["pdf", "doc", "docx"]

    extension = file.name.split(".")[-1].lower()

    if extension not in allowed_extensions:
        raise ValidationError("Only PDF or DOC resumes allowed.")
    

# =============== application model =============== 
class Application(models.Model):

    STATUS = (
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    )

    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE,
        related_name="applications"
    )

    candidate = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="applications"
    )

    resume = models.FileField(
        upload_to="resumes/",
        validators=[validate_resume]
    )

    cover_letter = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="applied"
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["job", "candidate"]

    def __str__(self):
        return f"{self.candidate} - {self.job}"