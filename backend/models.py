from django.db import models
from django.utils import timezone

# Create your models here.
class FrontendFileStatusModel(models.Model):
    filename = models.CharField(max_length=50, primary_key=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    enabled_date = models.DateTimeField(auto_now_add=True)
    in_use = models.BooleanField(default=False)

    @property
    def file_info(self):
        "return the file info list"
        file_info = [self.filename, timezone.localtime(self.modified_date).strftime('%Y-%m-%d %H:%M:%S'), timezone.localtime(self.enabled_date).strftime('%Y-%m-%d %H:%M:%S'), self.in_use]

        return file_info

class BackendFileStatusModel(models.Model):
    filename = models.CharField(max_length=50, primary_key=True)
    modified_date = models.DateTimeField(default="2007-04-30 00:00:00")
    enabled_date = models.DateTimeField(default="2007-04-30 00:00:00")
    in_use = models.BooleanField(default=False)

    @property
    def file_info(self):
        "return the file info list"
        file_info = [self.filename, timezone.localtime(self.modified_date).strftime('%Y-%m-%d %H:%M:%S'), timezone.localtime(self.enabled_date).strftime('%Y-%m-%d %H:%M:%S'), self.in_use]

        return file_info

class Test(models.Model):
    test = models.IntegerField()
