import csv
from datetime import datetime

FILE_NAME = "employee.csv"

FIELDNAMES = [
    "Name",
    "Role",
    "Domain",
    "Salary",
    "Joining Date",
    "Project Name"
]


def read_employees():
    try:
        with open(FILE_NAME, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        print("\nError: employee.csv was not found.")
        return []


def save_employees(employees):
    with open(FILE_NAME, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(employees)


def get_required_input(message):
    while True:
        value = input(message).strip()

        if value:
            return value

        print("This field cannot be empty. Please try again.")


def get_salary():
    while True:
        salary = input("Enter Salary: ").strip()

        try:
            salary_value = float(salary)

            if salary_value < 0:
                print("Salary cannot be negative.")
                continue

            return salary

        except ValueError:
            print("Invalid salary. Please enter a number.")


def get_date(message="Enter Joining Date (YYYY-MM-DD): "):
    while True:
        date = input(message).strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")


def view_employees():
    employees = read_employees()

    if not employees:
        print("\nNo employee records found.")
        return

    print("\n========== EMPLOYEE LIST ==========")

    for employee in employees:
        print("-----------------------------------")
        print(f"Name         : {employee['Name']}")
        print(f"Role         : {employee['Role']}")
        print(f"Domain       : {employee['Domain']}")
        print(f"Salary       : ₹{employee['Salary']}")
        print(f"Joining Date : {employee['Joining Date']}")
        print(f"Project      : {employee['Project Name']}")

    print("-----------------------------------")


def search_employee():
    search_name = get_required_input(
        "\nEnter employee name to search: "
    ).lower()

    employees = read_employees()
    found = False

    for employee in employees:
        if search_name in employee["Name"].lower():
            print("\n========== EMPLOYEE FOUND ==========")
            print(f"Name         : {employee['Name']}")
            print(f"Role         : {employee['Role']}")
            print(f"Domain       : {employee['Domain']}")
            print(f"Salary       : ₹{employee['Salary']}")
            print(f"Joining Date : {employee['Joining Date']}")
            print(f"Project      : {employee['Project Name']}")
            print("====================================")

            found = True

    if not found:
        print("\nEmployee not found.")


def add_employee():
    print("\n========== ADD EMPLOYEE ==========")

    employees = read_employees()

    name = get_required_input("Enter Name: ")

    # Check duplicate name
    for employee in employees:
        if employee["Name"].lower() == name.lower():
            print("\nAn employee with this name already exists.")
            return

    role = get_required_input("Enter Role: ")
    domain = get_required_input("Enter Domain: ")
    salary = get_salary()
    joining_date = get_date()
    project_name = get_required_input("Enter Project Name: ")

    new_employee = {
        "Name": name,
        "Role": role,
        "Domain": domain,
        "Salary": salary,
        "Joining Date": joining_date,
        "Project Name": project_name
    }

    employees.append(new_employee)
    save_employees(employees)

    print("\nEmployee added successfully! ✅")


def update_employee():
    search_name = get_required_input(
        "\nEnter employee name to update: "
    ).lower()

    employees = read_employees()
    found = False

    for employee in employees:
        if employee["Name"].lower() == search_name:
            found = True

            print("\n========== UPDATE EMPLOYEE ==========")
            print("Press Enter to keep the existing value.\n")

            new_role = input(
                f"Role [{employee['Role']}]: "
            ).strip()

            new_domain = input(
                f"Domain [{employee['Domain']}]: "
            ).strip()

            new_salary = input(
                f"Salary [{employee['Salary']}]: "
            ).strip()

            new_joining_date = input(
                f"Joining Date [{employee['Joining Date']}]: "
            ).strip()

            new_project = input(
                f"Project Name [{employee['Project Name']}]: "
            ).strip()

            if new_role:
                employee["Role"] = new_role

            if new_domain:
                employee["Domain"] = new_domain

            if new_salary:
                try:
                    salary_value = float(new_salary)

                    if salary_value < 0:
                        print("Invalid salary. Existing salary kept.")
                    else:
                        employee["Salary"] = new_salary

                except ValueError:
                    print("Invalid salary. Existing salary kept.")

            if new_joining_date:
                try:
                    datetime.strptime(
                        new_joining_date,
                        "%Y-%m-%d"
                    )
                    employee["Joining Date"] = new_joining_date

                except ValueError:
                    print(
                        "Invalid date. Existing date kept."
                    )

            if new_project:
                employee["Project Name"] = new_project

            break

    if not found:
        print("\nEmployee not found.")
        return

    save_employees(employees)

    print("\nEmployee updated successfully! ✅")


def delete_employee():
    search_name = get_required_input(
        "\nEnter employee name to delete: "
    ).lower()

    employees = read_employees()

    employee_to_delete = None

    for employee in employees:
        if employee["Name"].lower() == search_name:
            employee_to_delete = employee
            break

    if employee_to_delete is None:
        print("\nEmployee not found.")
        return

    print("\n========== EMPLOYEE ==========")
    print(f"Name    : {employee_to_delete['Name']}")
    print(f"Role    : {employee_to_delete['Role']}")
    print(f"Domain  : {employee_to_delete['Domain']}")
    print(f"Salary  : ₹{employee_to_delete['Salary']}")
    print(f"Project : {employee_to_delete['Project Name']}")
    print("==============================")

    confirm = input(
        "\nAre you sure you want to delete this employee? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("\nDelete cancelled.")
        return

    employees.remove(employee_to_delete)
    save_employees(employees)

    print("\nEmployee deleted successfully! ✅")


def menu():
    while True:
        print("\n===================================")
        print("      EMPLOYEE MANAGEMENT SYSTEM")
        print("===================================")
        print("1. View Employees")
        print("2. Search Employee")
        print("3. Add Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Exit")
        print("===================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_employees()

        elif choice == "2":
            search_employee()

        elif choice == "3":
            add_employee()

        elif choice == "4":
            update_employee()

        elif choice == "5":
            delete_employee()

        elif choice == "6":
            print("\nThank you for using Employee Management System!")
            break

        else:
            print("\nInvalid choice. Please enter 1-6.")


menu()