from enum import unique
from django.db import models
from core.models import TimeStampMixin
from django.contrib.auth.models import AbstractUser
from tracker.managers import UserManager
# Create your models here.
class User(TimeStampMixin, AbstractUser):
    email = models.EmailField(unique=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)
    def __str__(self) -> str:
        return f"{self.username}"

class Company(TimeStampMixin):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return self.name
    
class Employee(TimeStampMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='employees')

    def __str__(self):
        return self.name
    
class Device(TimeStampMixin):
    name = models.CharField(max_length=255)
    serial_no = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='devices')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class DeviceLog(TimeStampMixin):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='logs')
    checked_out_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='deviceHistory')
    checked_out_condition = models.CharField(max_length=255) # Device Condition
    checked_in_condition = models.CharField(max_length=255, null=True, blank=True) # Device Condition after return

    def __str__(self):
        return f"{self.device.name} - by:{self.checked_out_by.name}"

