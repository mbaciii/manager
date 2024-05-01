from django.db import models
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings

class UploadedFile(models.Model):
    file = models.FileField(upload_to='manager/')
    uploaded_at = models.DateTimeField(auto_now_add=True)