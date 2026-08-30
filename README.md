# Employee Management System

A Python-based desktop Employee Management System built with Tkinter.

The application provides employee management, role-based authentication,
secure password hashing, backup and restore, reporting, charts,
attendance management, import/export functionality, and activity logging.

---

## 🚀 Features

### 🔐 Authentication & Security

- Admin and Employee roles
- Secure password hashing using PBKDF2-HMAC-SHA256
- 600,000 PBKDF2 iterations
- Password verification
- Password change functionality
- Role-based access control
- Login protection against repeated failed attempts

---

### 👥 Employee Management

Admin users can:

- Add employees
- Update employees
- Delete employees
- Search employees
- Refresh employee data
- View employee information
- Manage employee records

Employee users have restricted access based on their role.

---

### 📊 Dashboard

The dashboard provides information such as:

- Total Employees
- IT Employees
- HR Employees
- Total Salary
- Average Salary

---

### 📈 Charts & Analytics

The system provides graphical information including:

- Employees by Domain
- Salary statistics
- Employee reports
- Domain-wise analysis
- Role-wise analysis
- Project-wise analysis

---

### 💾 Backup & Restore

The application provides data protection through:

- Automatic backup before Add
- Automatic backup before Update
- Automatic backup before Delete
- Manual backup
- Backup management
- Restore functionality
- Undo functionality

---

### 📥 Import & Export

Supported functionality includes:

- Import employee data
- Export employee data
- CSV support
- Excel XLSX support

---

### 📝 Activity Logging

Important application activities can be recorded, including:

- Login
- Logout
- Add employee
- Update employee
- Delete employee
- User management
- Password changes
- Backup operations
- Restore operations

---

### ⚙️ Settings

The application provides configurable application settings.

---

### ⌨️ Keyboard Shortcuts

Keyboard shortcuts are available for commonly used operations.

---

## 🛠️ Technologies Used

- Python
- Tkinter
- CSV
- JSON
- Matplotlib
- OpenPyXL
- PBKDF2-HMAC-SHA256
- Git
- GitHub

---

## 📂 Project Structure

```text
employee_management_system/
│
├── backups/
│   └── .gitkeep
│
├── exports/
│   └── .gitkeep
│
├── activity_log.csv
├── attendance.py
├── auth.py
├── employee.csv
├── gui.py
├── login.py
├── main.py
│
├── users.json
├── users.example.json
│
├── requirements.txt
├── README.md
└── .gitignore