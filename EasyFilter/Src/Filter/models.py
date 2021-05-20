from django.db import models

# Create your models here.
class TranscribeModel(models.Model):
    words = models.CharField(max_length=100, blank=True, null=True)
    video = models.FileField(upload_to='sample_inputs')