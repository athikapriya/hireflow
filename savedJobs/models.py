from django.db import models


# =============== saved job model =============== 
class SavedJob(models.Model):

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="saved_jobs"
    )

    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.CASCADE
    )

    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "job"]

    def __str__(self):
        return f"{self.user} saved {self.job}"