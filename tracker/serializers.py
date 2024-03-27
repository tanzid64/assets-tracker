from rest_framework import serializers
from tracker.models import Company, Employee, Device, DeviceLog, User

# User
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = User
        fields = ['email', 'password']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
# Company Serializer
class CompanyRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Company
        fields = ['id', 'name', 'username', 'email', 'password']

    def create(self, validated_data):
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'password': validated_data.pop('password')
        }
        owner = User.objects.create_user(**user_data)
        validated_data['owner'] = owner
        return super().create(validated_data)
    
class CompanySerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    class Meta:
        model = Company
        fields = "__all__"
# Employee
class CompanySerializerForEmployee(serializers.ModelSerializer):
    owner = UserSerializer(many=False)
    class Meta:
        model = Company
        fields = ['id', 'name','owner']
class EmployeeSerializer(serializers.ModelSerializer):
    company = CompanySerializerForEmployee(many=False, required=False)
    class Meta:
        model = Employee
        fields = "__all__"

# Device
class DeviceSerializer(serializers.ModelSerializer):
    owner = CompanySerializerForEmployee(many=False, required=False)
    class Meta:
        model = Device
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'PUT':
            self.fields['serial_no'].required = False
            self.fields['name'].required = False

class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method == 'PUT':
            self.fields['checked_out_condition'].required = False
            self.fields['device'].required = False
            self.fields['checked_out_by'].required = False
