from django.db import models
from django.utils.text import slugify


# =============== job category model =============== 
class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# =============== skill model =============== 
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    


# =============== job model =============== 
class Job(models.Model):

    JOB_TYPE = (
        ("full_time", "Full Time"),
        ("part_time", "Part time"),
        ("remote", "Remote"),
        ("internship", "Internship"),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('closed', 'Closed'),
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(max_length=220, unique=True, blank=True)

    description = models.TextField()

    company = models.ForeignKey(
        "companies.JobCompany",
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    employer = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="posted_jobs"
    )

    category = models.ForeignKey(
        JobCategory,
        on_delete=models.SET_NULL,
        null=True
    )

    skills = models.ManyToManyField(Skill, blank=True)

    location = models.CharField(max_length=200)

    salary = models.CharField(max_length=200, blank=True)

    job_type = models.CharField(max_length=20, choices=JOB_TYPE)

    experience_required = models.CharField(max_length=200, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="active"
    )

    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            num = 1

        while Job.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{num}"
            num += 1

        self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title