# HR Management System API

A Django REST Framework API for managing employees, departments, and attendance records.

## Installation

```bash
git clone https://github.com/EiadAhmed/hr_task
cd hr_task

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
python makemigration
python manage.py migrate

python manage.py createsuperuser

python manage.py runserver

http://127.0.0.1:8000/api/
```

## API Documentation

- **Swagger UI**: `GET /api/docs/swagger/`
- **ReDoc**: `GET /api/docs/redoc/`
- **OpenAPI Schema**: `GET /api/schema/`

## Authentication

### JWT Token Endpoints

#### Obtain Token Pair
- **URL**: `POST /api/token/`
- **Body**:
  ```json
  {
    "username": "user@example.com",
    "password": "your_password"
  }
  ```



## Employee Management

### Base URL: `/api/employees/`

#### List Employees
- **URL**: `GET /api/employees/`
- **Authentication**: Required
- **Permissions**: Any authenticated user
- **Query Parameters**:
  - `department`: Filter by department ID
  - `designation`: Filter by designation (hr/normal)
  - `user__is_active`: Filter by active status
  - `search`: Search by name, email, phone, designation
  - `ordering`: Order by name, join_date, salary

#### Get Employee Details
- **URL**: `GET /api/employees/{id}/`
- **Authentication**: Required
- **Permissions**: Any authenticated user

#### Create Employee
- **URL**: `POST /api/employees/`
- **Authentication**: Required
- **Permissions**: HR users only
- **Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "designation": "hr",
    "salary": "50000.00",
    "department": 1
  }
  ```

#### Update Employee
- **URL**: `PUT/PATCH /api/employees/{id}/`
- **Authentication**: Required
- **Permissions**: HR users only

## Department Management

### Base URL: `/api/departments/`

#### List Departments
- **URL**: `GET /api/departments/`
- **Authentication**: Required
- **Permissions**: Any authenticated user
- **Query Parameters**:
  - `name`: Filter by department name
  - `search`: Search by name
  - `ordering`: Order by name

#### Get Department Details
- **URL**: `GET /api/departments/{id}/`
- **Authentication**: Required
- **Permissions**: Any authenticated user

#### Create Department
- **URL**: `POST /api/departments/`
- **Authentication**: Required
- **Permissions**: HR users only
- **Body**:
  ```json
  {
    "name": "IT Department",
    "description": "Information Technology Department"
  }
  ```

#### Update Department
- **URL**: `PUT/PATCH /api/departments/{id}/`
- **Authentication**: Required
- **Permissions**: HR users only

## Attendance Management

### Base URL: `/api/attendances/`

#### List Attendance Records
- **URL**: `GET /api/attendances/`
- **Authentication**: Required
- **Permissions**: Any authenticated user
- **Query Parameters**:
  - `employee`: Filter by employee ID
  - `status`: Filter by status (Present/Absent/Leave)
  - `date`: Filter by specific date
  - `search`: Search by employee name or email
  - `ordering`: Order by date, employee name

#### Get Attendance Details
- **URL**: `GET /api/attendances/{id}/`
- **Authentication**: Required
- **Permissions**: Any authenticated user

#### Create Attendance Record
- **URL**: `POST /api/attendances/`
- **Authentication**: Required
- **Permissions**: HR users only
- **Body**:
  ```json
  {
    "employee": 1,
    "date": "2024-09-18",
    "status": "Present"
  }
  ```

#### Update Attendance Record
- **URL**: `PUT/PATCH /api/attendances/{id}/`
- **Authentication**: Required
- **Permissions**: HR users only

#### Monthly Attendance Report
- **URL**: `GET /api/attendances/monthly_attendance/`
- **Authentication**: Required
- **Permissions**: Any authenticated user
- **Description**: Get monthly attendance report for all employees (past 30 days)
- **Response**:
  ```json
  [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "1234567890",
      "designation": "hr",
      "join_date": "2024-01-01",
      "salary": "50000.00",
      "department": 1,
      "user": 1,
      "present": 20,
      "absent": 1,
      "leave": 1
    }
  ]
  ```

#### Employee Past Month Attendance
- **URL**: `GET /api/attendances/{id}/get_all_attendances_for_employee_in_past_month/`
- **Authentication**: Required
- **Permissions**: Any authenticated user
- **Description**: Get all attendance records for specific employee in past 30 days

## Department-wise Employees

### Get Employees by Department
- **URL**: `GET /api/departments/{id}/employees/`
- **Authentication**: Required
- **Permissions**: Any authenticated user
- **Description**: Fetch all employees in a specific department

## Permissions

### Permission Levels

1. **IsAuthenticated**: Any logged-in user
   - Can view all records (employees, departments, attendance)
   - Cannot create, update, or delete

2. **IsHR**: HR users only
   - Can create and update records
   - Cannot delete records
   - Can generate reports

3. **IsAdminUser**: Admin users only
   - Can perform all operations
   - Can delete records (if enabled)

### Permission Matrix

| Action | Employee | Department | Attendance |
|--------|----------|------------|------------|
| **List/View** | Authenticated | Authenticated | Authenticated |
| **Create** | HR | HR | HR |
| **Update** | HR | HR | HR |
| **Delete** | Disabled | Disabled | Disabled |

# Technical Requirements

- Django REST Framework
- JWT Authentication
- SQLite Database
- No duplicate attendance entries for same employee & date
- Search/filter employees by department or designation
- Monthly attendance report with Present/Absent/Leave counts

## API Testing

Test the endpoints using:
- **Swagger UI**: http://127.0.0.1:8000/api/docs/swagger/
- **ReDoc**: http://127.0.0.1:8000/api/docs/redoc/
- **Postman**: Import the API collection
