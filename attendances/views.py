from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from config.permissions import IsHR
from .models import Attendance
from .serializers import AttendanceSerializer

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
    