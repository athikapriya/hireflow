# third party imports
from django.contrib import admin

# local imports
from .models import User, JobCompany

admin.site.register(User)
admin.site.register(JobCompany)
