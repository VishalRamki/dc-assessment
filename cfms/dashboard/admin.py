from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Area, Complaint, ComplaintCategory, ComplaintStatus, ServicePlan, UserProfile

# Register your models here.
admin.site.register(Complaint)
admin.site.register(ComplaintCategory)
admin.site.register(ComplaintStatus)
admin.site.register(ServicePlan)
admin.site.register(Area)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class CustomerInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = "customer"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    def get_inlines(self, request, obj=None):
        if obj:  # editing an existing user
            if obj.groups.filter(name="Customer").exists():
                return [CustomerInline]
        return []


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)