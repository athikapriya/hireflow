# third party imports
from django.contrib import admin

# local imports
from .models import User


admin.site.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role')
    list_filter = ('role',)