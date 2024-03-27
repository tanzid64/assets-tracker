from asyncio import Condition
from rest_framework import viewsets, generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from tracker.models import Company, Employee, Device, DeviceLog,User
from tracker.serializers import UserLoginSerializer, CompanyRegistrationSerializer, CompanySerializer, EmployeeSerializer, DeviceSerializer, DeviceLogSerializer
from rest_framework.exceptions import NotFound
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from tracker.permission import ManageCompany
from rest_framework import serializers
# Create your views here.

# JWT Token
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# User
class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response({'token': token, 'message': "Login Successfull"}, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error':{'non_field_errors': ['Email or Password is not Valid']}
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Company
class CompanyView(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    permission_classes = [ManageCompany]
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CompanyRegistrationSerializer
        return CompanySerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.owner:
            return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)

class EmployeeView(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        try:
            company = Company.objects.get(owner=self.request.user)
            queryset = Employee.objects.filter(company=company)
            return queryset
        except Company.DoesNotExist:
            raise NotFound("Company not found")
        
    def perform_create(self, serializer):
        try:
            company = Company.objects.get(owner=self.request.user)
            serializer.save(company=company)
        except AttributeError:
            return Response({"error": "User doesn't have a company"}, status=status.HTTP_400_BAD_REQUEST)
        
# Device
class DeviceView(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    def get_queryset(self):
        try:
            company = Company.objects.get(owner=self.request.user)
            queryset = Device.objects.filter(owner=company.id)
            return queryset
        except Company.DoesNotExist:
            raise NotFound("Company not found")
    def perform_create(self, serializer):
        try:
            company = Company.objects.get(owner=self.request.user)
            serializer.save(owner=company)
        except AttributeError:
            return Response({"error": "User doesn't have a company"}, status=status.HTTP_400_BAD_REQUEST)

class DeviceLogView(generics.ListAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    def get_queryset(self):
        try:
            company = Company.objects.get(owner=self.request.user)
            queryset = DeviceLog.objects.filter(device__owner=company)
            return queryset
        except Company.DoesNotExist:
            raise NotFound("Company not found")

class DeviceCheckOutView(generics.CreateAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer

    def perform_create(self, serializer):
        condition = serializer.validated_data.get('checked_out_condition')
        device = serializer.validated_data.get('device')
        if not device.is_available:
            return Response(
                {"error": "Device already used by another employee."},
                status = status.HTTP_400_BAD_REQUEST
            )
        device.is_available = False
        device.save()
        return serializer.save(
            checked_out_condition = condition
        )

class DeviceCheckInView(generics.UpdateAPIView):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        try:
            instance = self.get_object()
            device = instance.device
            if instance.updated_at is not None:
                return Response(
                    {"error": "Device already returned."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            device.is_available = True
            device.save()
            serializer.save()
        except DeviceLog.DoesNotExist:
            return Response(
                {"error": "Device log not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
