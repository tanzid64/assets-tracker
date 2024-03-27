from urllib import response
from django.test import TestCase
from tracker.models import Employee, User, Company, Device, DeviceLog
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.utils import timezone

class CompanyViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_company(self):
        data = {
            "name": "Test Company",
            "username": "tanzid",
            "email": "tanzid@example.com",
            "password": "password123"
        
        }
        response = self.client.post('/api/companies/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertTrue(User.objects.filter(username="tanzid").exists())
        self.assertTrue(Company.objects.filter(name='Test Company').exists())

    def test_update_company(self):
        company = Company.objects.create(name="Test Company", owner = self.user)
        data = {
            "name": "updated Test Company"
        }
        response = self.client.put(f'/api/companies/{company.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company.refresh_from_db()
        self.assertEqual(company.name, 'updated Test Company')

    def test_destroy_company(self):
        company = Company.objects.create(name="Test Company", owner = self.user)
        response = self.client.delete(f'/api/companies/{company.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Company.objects.filter(name='Test Company').exists())

class EmployeeViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', username='testuser', password='password123')
        self.company = Company.objects.create(name="Test Company", owner = self.user)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.employee = Employee.objects.create(name='Employee 1', company=self.company)

    def test_create_employee(self):
        data = {
            "name": "testEmployee",
            "email": "employee@test.com",
            "address": "Mirpur-12"
        }
        response = self.client.post('/api/employees/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Employee.objects.filter(name='testEmployee').exists())
    def test_update_employee(self):
        employee = Employee.objects.create(name="testEmployee", email="employee@test.com", address="mirpur-12", company=self.company)
        data = {
            "name": "updatedTestEmployee"
        }
        response = self.client.put(f'/api/employees/{employee.pk}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        employee.refresh_from_db()
        self.assertEqual(employee.name, 'updatedTestEmployee')

    def test_get_queryset_with_company(self):
        response = self.client.get('/api/employees/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Employee 1')
    
class DeviceViewTestCase(APITestCase):
    def setUp(self):
        self.user_with_company = User.objects.create_user(email='user_with_company@test.com',username="user_with_company", password='password123')
        self.user_without_company = User.objects.create_user(email='user_without_company@test.com',username="user_without_company", password='password456')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_with_company)
        self.company = Company.objects.create(name='Test Company', owner=self.user_with_company)
        self.device = Device.objects.create(name='Device 1', owner=self.company)
    
    def test_get_queryset_with_company(self):
        response = self.client.get('/api/devices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Device 1')
    
    def test_get_queryset_without_company(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user_without_company)
        response = self.client.get('/api/devices/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_queryset_with_nonexistent_company(self):
        non_existing_user = User.objects.create_user(email='non_existing_user@test.com',username="non_existing_user", password='password789')
        self.client.logout()
        self.client.force_authenticate(user=non_existing_user)
        response = self.client.get('/api/devices/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_device(self):
        data = {
            "name":"Laptop",
            "serial_no":"L1245"
        }
        response = self.client.post('/api/devices/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Device.objects.filter(name='Laptop').exists())
    
    def test_create_device_without_company(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user_without_company)
        data = {
            'name': 'New Device'
        }
        response = self.client.post('/api/devices/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeviceLogViewTestCase(APITestCase):
    def setUp(self):
        self.user_with_company = User.objects.create_user(email='user_with_company@test.com',username="user_with_company", password='password123')
        self.user_without_company = User.objects.create_user(email='user_without_company@test.com',username="user_without_company", password='password456')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user_with_company)
        self.company = Company.objects.create(name='Test Company', owner=self.user_with_company)
        self.employee = Employee.objects.create(name='Employee 1', company=self.company)
        self.device = Device.objects.create(name='Test Device', owner=self.company)
        self.device_log = DeviceLog.objects.create(device=self.device, checked_out_by=self.employee, checked_out_condition="new")
    
    def test_get_queryset_with_company(self):
        response = self.client.get('/api/device-logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['checked_out_condition'], "new")
    
    def test_get_queryset_without_company(self):
        self.client.logout()
        self.client.force_authenticate(user=self.user_without_company)
        response = self.client.get('/api/device-logs/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_get_queryset_with_nonexistent_company(self):
        # Assuming there's no company associated with the user
        non_existing_user = User.objects.create_user(email='non_existing_user@test.com',username="non_existing_user", password='password789')
        self.client.logout()
        self.client.force_authenticate(user=non_existing_user)
        response = self.client.get('/api/device-logs/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class DeviceCheckOutViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(name='Test Company', owner=self.user)
        self.employee = Employee.objects.create(name='Employee 1', company=self.company)
        self.device = Device.objects.create(name='Test Device', is_available=True, owner=self.company)
    
    def test_device_checkout_success(self):
        data = {
            "device": self.device.id,
            "checked_out_by": self.employee.id,
            "checked_out_condition": "new"
        }
        response = self.client.post('/api/check-out/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)      
        self.assertTrue(DeviceLog.objects.filter(device=self.device).exists())      
        device_log = DeviceLog.objects.get(device=self.device)
        self.assertAlmostEqual(device_log.created_at.timestamp(), timezone.now().timestamp(), delta=10)
        self.device.refresh_from_db()
        self.assertFalse(self.device.is_available)
    
    def test_device_checkout_failure(self):
        self.device.is_available = False
        self.device.save()
        
        data = {
            "device": self.device.id,
            "checked_out_by": self.employee.id,
            "checked_out_condition": "new"
        }
        response = self.client.post('/api/check-out/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeviceCheckInViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='testuser@test.com', username='testuser', password='password123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.company = Company.objects.create(name='Test Company', owner=self.user)
        self.employee = Employee.objects.create(name='Employee 1', company=self.company)
        self.device = Device.objects.create(name='Test Device', is_available=True, owner=self.company)
        self.device_log = DeviceLog.objects.create(device=self.device, checked_out_by=self.employee)
    
    def test_device_check_in_success(self):
        response = self.client.put(f'/api/check-in/{self.device_log.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if device availability is updated
        self.device.refresh_from_db()
        self.assertTrue(self.device.is_available)
    
    def test_device_check_in_failure_device_log_not_found(self):
        non_existing_device_log_id = 9999
        response = self.client.put(f'/api/check-in/{non_existing_device_log_id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
