# third party imports
from django.contrib import admin

# local imports
from .models import User, JobCompany, JobCategory, Job, Application, SavedJob, Skill, CandidateProfile, EmployerProfile

admin.site.register(User)
admin.site.register(JobCompany)
admin.site.register(JobCategory)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(SavedJob)
admin.site.register(Skill)
admin.site.register(CandidateProfile)
admin.site.register(EmployerProfile)
