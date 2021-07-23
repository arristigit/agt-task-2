from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField

# Create your models here.
class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.URLField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    zip = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username
    
class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pic = models.URLField()
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    zip = models.CharField(max_length=250)
    
    def __str__(self):
        return self.user.username

class Post(models.Model):    
    author = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    title = models.CharField(max_length=5000)
    image = models.URLField()
    category = models.CharField(max_length=500)
    summary = models.CharField(max_length=3000)
    content = models.CharField(max_length=50000)
    draft = models.BooleanField(default=False)

    def __str__(self):
        return self.title +" - "+ self.category +" - "+ self.author.user.first_name
