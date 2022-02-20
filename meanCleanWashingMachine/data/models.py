from django.db import models

# Create your models here.
class Data(models.Model):
    Name = models.CharField(max_length=300)
    Description = models.CharField(max_length=500)
    Image = models.ImageField()
