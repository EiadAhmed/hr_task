from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, Employee
import secrets
import string
from django.db import transaction


# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     """Custom User admin configuration"""
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
#     search_fields = ('username', 'email', 'first_name', 'last_name')
#     ordering = ('-date_joined',)
    
#     fieldsets = (
#         (None, {'fields': ('username', 'password')}),
#         ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
#         ('Permissions', {
#             'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
#         }),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#     )


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Employee admin configuration"""
    list_display = ('name', 'email', 'designation', 'department', 'join_date', 'salary', 'is_active')
    list_filter = ('designation', 'department', 'join_date', 'user__is_active')
    search_fields = ('name', 'email', 'phone')
    ordering = ('name',)
    readonly_fields = ('join_date',)
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Employment Details', {
            'fields': ('designation', 'department', 'salary', 'join_date')
        }),
    )
    
    def is_active(self, obj):
        """Show if the associated user is active"""
        return obj.user.is_active
    is_active.boolean = True
    is_active.short_description = 'Active'
    
    def get_queryset(self, request):
        """Optimize queries by selecting related objects"""
        return super().get_queryset(request).select_related('department', 'user')
    
    def save_model(self, request, obj, form, change):
        """Custom save logic for creating and updating employees"""
        with transaction.atomic():
            if not change:  # Creating a new employee
                # Create a new user for the employee
                email = form.cleaned_data['email']
                password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    is_active=True,
                    is_staff=False
                )
                print(f"New employee created - Email: {email}, Password: {password}")
                obj.user = user
            else:  # Updating an existing employee
                # Update the existing user's email if it changed
                if obj.user and obj.user.email != form.cleaned_data['email']:
                    obj.user.email = form.cleaned_data['email']
                    obj.user.username = form.cleaned_data['email']
                    obj.user.save()
                    print(f"Updated user email to: {form.cleaned_data['email']}")
            
            # Save the employee object
            super().save_model(request, obj, form, change)
