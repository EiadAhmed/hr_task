from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['password','last_login','is_active','is_staff','is_superuser','date_joined','groups','user_permissions']