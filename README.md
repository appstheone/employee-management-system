# Employee Management System

A desktop-based Employee Management System developed using Python and Tkinter.

The application provides employee management, role-based authentication,
attendance management, dashboard statistics, charts, backup and restore,
user management, and activity logging.

---

## Features

### Authentication & Security
- Secure login system
- Admin and Employee roles
- Password hashing using PBKDF2-HMAC-SHA256
- Role-based access control
- Change password functionality

### Employee Management
- Add employees
- Update employee information
- Delete employees
- Search employees
- View employee details

### Dashboard
- Total employees
- IT employees
- HR employees
- Total salary
- Average salary
- Employees by domain chart
- Salary chart

### Attendance Management
- Admin-only attendance management
- Select employee
- Mark Present, Absent, or Leave
- Check-in time
- Check-out time
- Date validation
- Duplicate attendance prevention
- Search attendance records
- Delete attendance records
- Attendance data stored locally

### User Management
- Manage application users
- Admin and Employee roles
- Secure password storage

### Data Management
- Backup employee data
- Restore employee data
- CSV-based data storage
- Activity logging

---

## Technologies Used

- Python
- Tkinter
- CSV
- JSON
- Matplotlib
- PBKDF2-HMAC-SHA256
- Git
- GitHub

---

## Project Structure

```text
employee-management-system/
│
├── backups/
│   └── .gitkeep
│
├── exports/
│   └── .gitkeep
│
├── activity_log.csv
├── attendence.py
├── auth.py
├── employee.csv
├── gui.py
├── login.py
├── main.py
│
├── users.example.json
├── requirements.txt
├── README.md
└── .gitignore


---

## Screenshots

### Login

![Login Screen](screenshots/login.png)

### Admin Dashboard

![Admin Dashboard](screenshots/dashboard.png)

### Employee Management

![Employee Management](screenshots/employees.png)

### Charts

![Charts](screenshots/charts.png)

### Attendance Management

![Attendance Management](screenshots/attendance.png)

### User Management

![User Management](screenshots/users.png)

### Backup and Restore

![Backup and Restore](screenshots/backup.png)
