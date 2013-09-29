from django.db import models

# Create your models here.

class Class(models.Model):

    classid = models.CharField(primary_key=True, max_length=200)
    term = models.CharField(max_length=500)
    subject = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    number = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)

class Lecture(models.Model):

    sectionnumber = models.CharField(primary_key=True, max_length=200)

    _class = models.ForeignKey(Class)
    start_time = models.TimeField()
    end_time = models.TimeField()
    class_type = models.CharField(max_length=500)
    days = models.CharField(max_length=500)
    credits = models.CharField(max_length=500)
    instructors = models.CharField(max_length=500)
    classnum = models.CharField(max_length=500)
    mode = models.CharField(max_length=500)
    location = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now=True)





