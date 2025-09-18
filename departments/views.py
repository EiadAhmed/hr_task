from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from config.permissions import IsHR
from .models import Department
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
            permission_classes = [IsAdminUser]  # Only HR/Admin can create/update employees
        elif self.action in ['create', 'update', 'partial_update']:
            permission_classes = [IsHR]
        else:
            permission_classes = [IsAuthenticated]  # All authenticated users can view
        return [permission() for permission in permission_classes]
    