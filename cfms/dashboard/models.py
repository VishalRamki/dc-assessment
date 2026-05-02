from django.db import models
from django.conf import settings

# Create your models here.

class ComplaintStatus(models.Model):
    name = models.CharField(max_length=128)

class ComplaintCategory(models.Model):
    name = models.CharField(max_length=128)

class Notes(models.Model):
    description = models.CharField(max_length=1024)

class Complaint(models.Model):
    
    description = models.CharField(max_length=1024)
    sub_date = models.DateTimeField("date submitted")
    last_update_date = models.DateTimeField("last updated timestamp")

    ## reference
    customer_account_ref = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assigned_complaints'
    )

    assigned_agent_ref = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='customer_complaints'
    )

    complaint_category_ref = models.ForeignKey(ComplaintCategory, on_delete=models.CASCADE)
    complaint_status_ref = models.ForeignKey(ComplaintStatus, on_delete=models.CASCADE)

    notes = models.ManyToManyField(Notes)