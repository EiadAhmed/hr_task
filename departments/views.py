from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from config.permissions import IsHR
from .models import Department
from employees.models import Employee
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from employees.serializers import EmployeeSerializer
from .serializers import DepartmentSerializer

# Create your views here.

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']
    search_fields = ['name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in [ 'destroy']:
            permission_classes = [IsAdminUser]  
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsHR]
        else:
            permission_classes = [IsAuthenticated] 
        return [permission() for permission in permission_classes]
    @action(detail=True, methods=['get'])
    def get_all_employees_in_department(self, request, *args, **kwargs):
        return Response(EmployeeSerializer(Employee.objects.filter(department=self.kwargs['pk']),many=True).data,status=status.HTTP_200_OK)
    