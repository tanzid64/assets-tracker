from django.urls import path, include
from tracker.views import UserLoginView, CompanyView, EmployeeView, DeviceView, DeviceLogView, DeviceCheckInView, DeviceCheckOutView,DeviceCheckInView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'companies', CompanyView, basename='company-api') 
router.register(r'employees', EmployeeView, basename='employee-api')
router.register(r'devices', DeviceView, basename='device-api')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLoginView.as_view(), name='login-api'),
    path('device-logs/', DeviceLogView.as_view(), name='device-logs-api'),
    path('check-out/', DeviceCheckOutView.as_view(), name="check-out"),
    path('check-in/<pk>/', DeviceCheckInView.as_view(), name="check-in"),
]
