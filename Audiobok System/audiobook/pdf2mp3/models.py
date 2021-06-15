from django.db import models
from django.forms import ModelForm
import datetime

# Create your models here.

class Audiobookuser(models.Model):

    name = models.CharField(max_length=100)
    sname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
    cpassword = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

class Pdf(models.Model):
    dt = models.DateTimeField()
    u = models.ForeignKey(Audiobookuser, on_delete=models.CASCADE)
    pname = models.CharField(max_length=10)
    pdf = models.FileField()
    arange = models.CharField(max_length=10)
    aname = models.CharField(max_length=10)
    mp3 = models.FileField()

    def __unicode__(self):
        return self.pname

class Pdftemp(models.Model):
    ddt = models.DateTimeField()
    uu = models.ForeignKey(Audiobookuser,on_delete=models.CASCADE)
    ppname = models.CharField(max_length=10)
    ppdf = models.FileField()
    aarange = models.CharField(max_length=10)
    aaname = models.CharField(max_length=10)
    mmp3 = models.FileField()
    
    def __unicode__(self):
        return self.ppname

