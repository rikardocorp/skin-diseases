import datetime
from django.db import models
from django.utils import timezone
from slugify import slugify
from django.contrib.auth.models import User
# Create your models here.


class Sourcedata(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500, default='')
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    state = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=timezone.now())
    detail = models.CharField(max_length=500, default='')
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def __str__(self):
        return self.name

    def countImage(self):
        idx = self.id
        return Imageskin.objects.all().filter(disease__category=idx).count()


class Disease(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    detail = models.CharField(max_length=1000,blank=True)
    state = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.name

    def directory(self):
        return slugify(self.name)

    def cover(self):
        aux = self.imageskin_set.last()
        if aux:
            return aux.docfile.url
        else:
            return ""

    def count_images(self):
        return self.imageskin_set.all().count()


class Imageskin(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    sourcedata = models.ForeignKey(Sourcedata, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    docfile = models.FileField(upload_to='dataset', null=True, blank=True)
    description = models.CharField(max_length=1000, default='')
    state = models.BooleanField(default=True)
    select = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id)+"_"+self.name


class Commentimage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imageskin = models.ForeignKey(Imageskin, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    state = models.IntegerField(default=0)
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id)+'_'+self.text+'_'+str(self.user.username)


class Commentuser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    commentimage = models.ForeignKey(Commentimage, on_delete=models.CASCADE)
    state = models.BooleanField(default=True)
    pub_date = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return str(self.id)+'_C:'+str(self.commentimage.id)+'_U:' + str(self.user.username)


# a = Imageskin.objects.values('disease__category').annotate(Count('disease__category'))
# a = Imageskin.objects.values('disease','disease__category').annotate(Count('disease'))#

# OBTENER TODAS LAS IMAGENES DE UNA CATEGORIA
# i = Imageskin.objects.all().filter(disease__category=5)
