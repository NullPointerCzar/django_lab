from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class UserProfile(models.Model):
    name = models.CharField(max_length=40)
    patient_id = models.CharField(max_length=20)
    mobile = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    address = models.TextField()
    dob = models.DateField()
    doctor_name = models.CharField(max_length=50)

    username = models.CharField(max_length=50)
    email = models.EmailField()
    password = models.CharField(max_length=50)

    hobbies = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    appointment = models.DateTimeField()

    file = models.FileField(upload_to='uploads/')