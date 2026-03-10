# third party imports
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


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
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    

# =============== job category model =============== 
class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


# =============== Job Model =============== 
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
    company = models.ForeignKey(JobCompany, on_delete=models.CASCADE, related_name="jobs")
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_jobs")
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200)
    salary = models.CharField(max_length=200, blank=True)
    job_type = models.CharField(max_length=200, choices=JOB_TYPE)
    experience_required = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



# =============== Application =============== 
class Application(models.Model):
    STATUS = (
        ("applied", "Applied"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
        ("hired", "Hired"),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="resumes/")
    cover_letter = models.TextField(blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default="applied")
    applied_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        unique_together = ['job', 'candidate']

    def __str__(self):
        return f"{self.candidate} - {self.job}"



# =============== Saved jobs model =============== 
class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} saved {self.job}"



# =============== skill model =============== 
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


# =============== candidate_profile model =============== 
class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    skills = models.ManyToManyField(Skill, blank=True) 
    experience = models.TextField(blank=True)
    resume = models.FileField(upload_to='candidate_resumes/', blank=True, null=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    location = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.username


# =============== employer profile model =============== 
class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=200)
    company = models.ForeignKey(JobCompany, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username