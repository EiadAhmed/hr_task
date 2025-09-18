from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from config.permissions import IsHR
from .models import Attendance
from .serializers import AttendanceSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from employees.models import Employee
from employees.serializers import EmployeeSerializer
# Create your views here.
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['employee', 'status', 'date']
    ordering_fields = ['date', 'employee__name']
    ordering = ['-date', 'employee__name']
    search_fields = ['employee__name', 'employee__email']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['destroy']:
            permission_classes = [IsAdminUser]  # Only Admin can delete attendance
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsHR]  # Only HR can create/update attendance
        else:
            permission_classes = [IsAuthenticated]  # All authenticated users can view
        return [permission() for permission in permission_classes]
    @action(detail=False, methods=['get'])
    def monthly_attendance(self, request, *args, **kwargs):
        employees = Employee.objects.all()
        report_data = []
        
        for employee in employees:
            # Get attendance records for the past 30 days
            attendance_queryset = Attendance.objects.filter(
                employee=employee, 
                date__gte=timezone.now().date() - timedelta(days=30)
            )
            
            # Count attendance by status (using QuerySet, not serialized data)
            present_count = attendance_queryset.filter(status='Present').count()
            absent_count = attendance_queryset.filter(status='Absent').count()
            leave_count = attendance_queryset.filter(status='Leave').count()
            
            # Get employee data
            employee_data = EmployeeSerializer(employee).data
            
            # Add attendance counts to employee data
            employee_data['present'] = present_count
            employee_data['absent'] = absent_count
            employee_data['leave'] = leave_count
            
            report_data.append(employee_data)
        
        return Response(report_data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])

    def get_all_attendances_for_employee_in_past_month(self, request, *args, **kwargs):
        return Response(AttendanceSerializer(Attendance.objects.filter(employee=self.kwargs['pk'], date__gte=timezone.now().date() - timedelta(days=30)),many=True).data,status=status.HTTP_200_OK)