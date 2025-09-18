from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string
from departments.models import Department
import secrets
import string
# Create your models here.
class User(AbstractUser):
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    pass
class Employee(models.Model):
    # Override the groups and user_permissions fields to avoid conflicts

    employee_type = {
        ('hr', 'HR'),
        ('normal', 'Normal'),
    }
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20,unique=True)
    designation = models.CharField(max_length=100, choices=employee_type)
    join_date = models.DateField(auto_now_add=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee')
    def save(self, *args, **kwargs):

        password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
        self.password = password
        super().save(*args, **kwargs)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.designation}"
