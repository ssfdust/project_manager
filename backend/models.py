from django.db import models

# Create your models here.
class FrontendFileStatusModel(models.Model):
    filename = models.CharField(max_length=50)
    create_date = models.DateTimeField(auto_now_add=True)
    in_use = models.BooleanField()
