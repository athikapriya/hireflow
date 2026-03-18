# third party imports
from django.urls import path

# local imports
from . import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
]
