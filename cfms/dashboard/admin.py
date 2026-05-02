from django.contrib import admin

from .models import Complaint, ComplaintCategory, ComplaintStatus

# Register your models here.
admin.site.register(Complaint)
admin.site.register(ComplaintCategory)
admin.site.register(ComplaintStatus)