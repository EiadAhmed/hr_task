from django.contrib import admin
from django.utils.html import format_html
from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Department admin configuration"""
    list_display = ('name', 'employee_count', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def employee_count(self, obj):
        """Show the number of employees in this department"""
        count = obj.employees.count()
        if count > 0:
            return format_html(
                '<a href="?department__id__exact={}">{} employees</a>',
                obj.id,
                count
            )
        return f"{count} employees"
    employee_count.short_description = 'Employees'
    employee_count.admin_order_field = 'employees__count'
    
    def get_queryset(self, request):
        """Optimize queries by prefetching related employees"""
        return super().get_queryset(request).prefetch_related('employees')
