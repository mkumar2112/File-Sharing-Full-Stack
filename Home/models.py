from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
# import datetime
# from django.utils import timezone
# import os
from django.conf import settings  # Import settings to access MEDIA_ROOT

class Files(models.Model):
    id = models.AutoField(primary_key=True)
    File = models.FileField(upload_to='OpsU/', validators=[FileExtensionValidator(['docx', 'pptx', 'xlsx', 'pdf'])])
    Note = models.CharField(max_length=500)
    key = models.CharField(max_length=16)
    Email = models.EmailField(max_length=254)

    def file_name_substring(self):
        return str(self.File)[5:] if self.File else ''

    def __str__(self):
        return f"File ID: {self.id}, Key: {self.key}"

  
