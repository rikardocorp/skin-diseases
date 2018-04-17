import datetime
from django.db import models
from django.utils import timezone
from catalogo.models import Imageskin
# Create your models here.


class CropImage(models.Model):
    imageskin = models.ForeignKey(Imageskin, on_delete=models.CASCADE)
    path = models.CharField(max_length=200, default='')
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    originalWidth = models.IntegerField(default=0)
    originalHeight = models.IntegerField(default=0)
    transform = models.CharField(max_length=200, default='')

    def __str__(self):
        return str(self.id)+'_'+str(self.imageskin.name)

