from django.db import models

from dashboard.models import settings

# Create your models here.
class Message(models.Model):
    prompt = models.CharField(max_length=512)
    response = models.TextField(blank=True, null=True)
    user_ref = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    def __str__(self):
        return self.prompt