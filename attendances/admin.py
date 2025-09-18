from django.contrib import admin
from .models import Attendance

# Register your models here.

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['employee', 'date', 'status', 'created_at']
    list_filter = ['status', 'date', 'employee__department']
    search_fields = ['employee__name', 'employee__email']
    ordering = ['-date', 'employee__name']
    list_per_page = 25
    date_hierarchy = 'date'
