# backend/court_api/models.py
from django.db import models

class CaseQueryLog(models.Model):
    case_type = models.CharField(max_length=20)
    case_number = models.CharField(max_length=50)
    filing_year = models.CharField(max_length=10)
    raw_html = models.TextField()
    queried_at = models.DateTimeField(auto_now_add=True)
