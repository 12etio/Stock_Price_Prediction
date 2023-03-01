from django.db import models
from django.contrib.auth.models import User

class UserRequest(models.Model):
    request_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symbol = models.CharField(max_length=10, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    num_epochs = models.IntegerField(null=True, blank=True)
    batch_size = models.IntegerField(null=True, blank=True)
    

# class User(models.Model):
#     firstname = models.CharField(max_length=255, null=True)
#     lastname = models.CharField(max_length=255, null=True)
#     phone = models.IntegerField(null=True)
#     email = models.EmailField(max_length=255, null=True)
#     username = models.CharField(max_length=255, null=True)
#     password = models.CharField(max_length=255, null=True)

# class User(AbstractUser):
#     is_student = models.BooleanField(default=False)
#     is_teacher = models.BooleanField(default=False)
#     first_name = models.CharField(max_length=80)
#     last_name = models.CharField(max_length=80)

# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     phone_number = models.CharField(max_length=10)
#     class_name = models.CharField(max_length=100)

# class Teacher(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
#     phone_number = models.CharField(max_length=10)
#     department = models.CharField(max_length=30)