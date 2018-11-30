from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    rollNo = models.CharField(primary_key=True, max_length=20)
    lastState = models.CharField(max_length=200)
    lastUpdated = models.DateTimeField()
    phoneNumber = models.CharField(max_length=50)
    comments = models.CharField(max_length=2000)


class Company(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    description = models.CharField(max_length=1000)


class State(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    updatedOn = models.DateTimeField(auto_now_add=True)
    updatedBy = models.ForeignKey(User)
    company = models.ForeignKey(Company)


class Update(models.Model):
    description = models.CharField(max_length=1000)
    addedOn = models.DateTimeField(auto_now_add=True)


class RememberPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    companyPreference = models.ForeignKey(Company, on_delete=models.CASCADE)