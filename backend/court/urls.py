from django.urls import path
from .views import fetch_case_data

urlpatterns = [
    path("api/fetch-case/", fetch_case_data),
    

]
