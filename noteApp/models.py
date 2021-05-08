from django.db import models

# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, max_length=500)
    username = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)





