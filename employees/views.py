from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Employee
from .serializers import EmployeeSerializer  
from config.permissions import IsHR
import secrets
import string
from django.db import transaction
from .models import User
# Create your views here.

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['department', 'designation', 'user__is_active']
    search_fields = ['name', 'email', 'phone', 'designation']
    ordering_fields = ['name', 'join_date', 'salary']
    ordering = ['name']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in [ 'destroy']:
            permission_classes = [IsAdminUser]  # Only admin can create/update employees
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsHR]
        else:
            permission_classes = [IsAuthenticated]  # All authenticated users can view
        return [permission() for permission in permission_classes]
    
    def create(self, request, *args, **kwargs):
        """Override create to return the generated password"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        employee = serializer.save()
        
        # Return the employee data with the generated password
        response_data = serializer.data
        with transaction.atomic():

                # 3️ Create a global admin user for the company
                email = form.cleaned_data['email']  # Get email from form
                password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    is_active=True,
                    is_staff=True
                )
            
                print(password)
                print(email)

                employee.user = user
                employee.save()
        
        return Response(response_data, status=status.HTTP_201_CREATED)
    
