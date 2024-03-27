from django.contrib import admin
from tracker.models import Company, Device, DeviceLog, Employee,User
# Register your models here.
admin.site.register(User)
admin.site.register(Company)
admin.site.register(Employee)
admin.site.register(Device)
admin.site.register(DeviceLog)