from django.db import models

# Create your models here.

def name_file(instance, filename):
    return '/'.join(['images', str(instance.name), filename])

class ImageModel(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(upload_to='images')
