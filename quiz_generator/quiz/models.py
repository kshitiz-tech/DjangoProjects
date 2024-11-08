from django.db import models


# Create your models here.
class UploadFile(models.Model):
    file = models.FileField(blank = True, null = True)


