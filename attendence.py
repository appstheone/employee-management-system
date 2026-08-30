import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import date, datetime


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ATTENDANCE_FILE = os.path.join(
    BASE_DIR,
    "attendance.csv"
)

EMPLOYEE_FILE = os.path.join(
    BASE_DIR,
    "employee.csv"
)

ATTENDANCE_HEADERS = [
    "Employee ID",
    "Employee Name",
    "Date",
    "Check In",
    "Check Out",
    "Status"
]

EMPLOYEE_HEADERS = [
    "Name",
    "Role",
    "Domain",
    "Salary",
    "Joining Date",
    "Project Name"
]


# ============================================================
# LOAD ATTENDANCE
# ============================================================

def load_attendance():

    records = []

    if not os.path.exists(
        ATTENDANCE_FILE
    ):
        return records

    try:

        with open(
            ATTENDANCE_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                records.append({
                    field: str(
                        row.get(
                            field,
                            ""
                        )
                    ).strip()
                    for field in ATTENDANCE_HEADERS
                })

    except Exception as error:

        messagebox.showerror(
            "Attendance File Error",
            "Could not read attendance.csv.\n\n"
            + str(error)
        )

    return records


# ============================================================
# SAVE ATTENDANCE
# ============================================================

def save_attendance(records):

    try:

        with open(
            ATTENDANCE_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=ATTENDANCE_HEADERS
            )

            writer.writeheader()

            writer.writerows(
                records
            )

        return True

    except Exception as error:

        messagebox.showerror(
            "Attendance Save Error",
            "Could not save attendance.csv.\n\n"
            + str(error)
        )

        return False


# ============================================================
# LOAD EMPLOYEES DIRECTLY FROM CSV
# ============================================================

def load_employees_from_csv():

    employees = []

    if not os.path.exists(
        EMPLOYEE_FILE
    ):
        return employees

    try:

        with open(
            EMPLOYEE_FILE,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(
                file
            )

            for index, row in enumerate(
                reader,
                start=1
            ):

                name = str(
                    row.get(
                        "Name",
                        ""
                    )
                ).strip()

                if not name:
                    continue

                employee_id = str(
                    row.get(
                        "Employee ID",
                        ""
                    )
                ).strip()

                # ------------------------------------------------
                # If Employee ID exists in CSV, use it.
                # Otherwise generate a stable-looking ID based
                # on the current record.
                # ------------------------------------------------

                if not employee_id:

                    employee_id = (
                        f"EMP{index:03d}"
                    )

                employees.append({
                    "id": employee_id,
                    "name": name
                })

    except Exception as error:

        messagebox.showerror(
            "Employee File Error",
            "Could not read employee.csv.\n\n"
            + str(error)
        )

    return employees


# ============================================================
# BUILD EMPLOYEE LIST
# ============================================================

def build_employee_list(
    employees
):

    result = []

    used_ids = set()

    for index, employee in enumerate(
        employees,
        start=1
    ):

        if not isinstance(
            employee,
            dict
        ):
            continue

        name = str(
            employee.get(
                "Name",
                employee.get(
                    "name",
                    ""
                )
            )
        ).strip()

        if not name:
            continue

        employee_id = str(
            employee.get(
                "Employee ID",
                employee.get(
                    "id",
                    ""
                )
            )
        ).strip()

        if not employee_id:

            employee_id = (
                f"EMP{index:03d}"
            )

        # --------------------------------------------------------
        # Avoid duplicate IDs
        # --------------------------------------------------------

        if employee_id in used_ids:

            employee_id = (
                f"EMP{index:03d}"
            )

        used_ids.add(
            employee_id
        )

        result.append({
            "id": employee_id,
            "name": name
        })

    return result


# ============================================================
# ATTENDANCE WINDOW
# ============================================================

def open_attendance_window(
    parent=None,
    employees=None,
    username="",
    role="ADMIN",
    log_callback=None
):

    role = str(
        role
    ).strip().upper()

    # ========================================================
    # ADMIN ONLY
    # ========================================================

    if role != "ADMIN":

        messagebox.showerror(
            "Access Denied",
            "Only administrators can manage attendance."
        )

        return None

    # ========================================================
    # EMPLOYEE DATA
    # ========================================================

    if employees is None:

        employees = load_employees_from_csv()

    employee_list = build_employee_list(
        employees
    )

    # ========================================================
    # WINDOW
    # ========================================================

    if parent is None:

        window = tk.Tk()

    else:

        window = tk.Toplevel(
            parent
        )

    window.title(
        "Employee Attendance System"
    )

    window.geometry(
        "1250x760"
    )

    window.minsize(
        1050,
        650
    )

    if parent is not None:

        window.transient(
            parent
        )

        window.grab_set()

    # ========================================================
    # LOCAL LOG FUNCTION
    # ========================================================

    def log(
        action,
        details
    ):

        if callable(
            log_callback
        ):

            try:

                log_callback(
                    username,
                    role,
                    action,
                    details
                )

            except Exception:
                pass

    # ========================================================
    # GET SELECTED EMPLOYEE
    # ========================================================

    def get_selected_employee():

        selected = (
            employee_combo.get().strip()
        )

        for employee in employee_list:

            display = (
                f"{employee['id']} - "
                f"{employee['name']}"
            )

            if selected == display:

                return employee

        return None

    # ========================================================
    # DATE
    # ========================================================

    def set_default_date():

        date_entry.delete(
            0,
            tk.END
        )

        date_entry.insert(
            0,
            date.today().strftime(
                "%Y-%m-%d"
            )
        )

    # ========================================================
    # CURRENT TIME
    # ========================================================

    def set_current_time(
        entry
    ):

        entry.delete(
            0,
            tk.END
        )

        entry.insert(
            0,
            datetime.now().strftime(
                "%H:%M"
            )
        )

    # ========================================================
    # CLEAR FORM
    # ========================================================

    def clear_fields():

        employee_combo.set(
            ""
        )

        date_entry.delete(
            0,
            tk.END
        )

        date_entry.insert(
            0,
            date.today().strftime(
                "%Y-%m-%d"
            )
        )

        checkin_entry.delete(
            0,
            tk.END
        )

        checkout_entry.delete(
            0,
            tk.END
        )

        status_combo.set(
            "Present"
        )

        status_bar.config(
            text="Form cleared."
        )

        if employee_list:

            employee_combo.focus_set()

    # ========================================================
    # EMPLOYEE SELECTED
    # ========================================================

    def on_employee_selected(
        event=None
    ):

        employee = (
            get_selected_employee()
        )

        if employee is not None:

            status_bar.config(
                text=(
                    f"Selected: "
                    f"{employee['id']} - "
                    f"{employee['name']}"
                )
            )

    # ========================================================
    # DISPLAY RECORDS
    # ========================================================

    def display_records(
        records
    ):

        for item in attendance_tree.get_children():

            attendance_tree.delete(
                item
            )

        for record in records:

            attendance_tree.insert(
                "",
                tk.END,
                values=(
                    record.get(
                        "Employee ID",
                        ""
                    ),
                    record.get(
                        "Employee Name",
                        ""
                    ),
                    record.get(
                        "Date",
                        ""
                    ),
                    record.get(
                        "Check In",
                        ""
                    ),
                    record.get(
                        "Check Out",
                        ""
                    ),
                    record.get(
                        "Status",
                        ""
                    )
                )
            )

        total_label.config(
            text=str(
                len(records)
            )
        )

    # ========================================================
    # REFRESH
    # ========================================================

    def refresh_attendance():

        records = load_attendance()

        display_records(
            records
        )

        status_bar.config(
            text=(
                f"Showing {len(records)} "
                "attendance record(s)."
            )
        )

    # ========================================================
    # MARK ATTENDANCE
    # ========================================================

    def add_attendance():

        employee = (
            get_selected_employee()
        )

        if employee is None:

            messagebox.showerror(
                "Error",
                "Please select an employee.",
                parent=window
            )

            employee_combo.focus_set()

            return

        employee_id = employee[
            "id"
        ]

        employee_name = employee[
            "name"
        ]

        attendance_date = (
            date_entry.get().strip()
        )

        check_in = (
            checkin_entry.get().strip()
        )

        check_out = (
            checkout_entry.get().strip()
        )

        status = (
            status_combo.get().strip()
        )

        # ====================================================
        # REQUIRED FIELDS
        # ====================================================

        if not attendance_date:

            messagebox.showerror(
                "Error",
                "Please enter Date.",
                parent=window
            )

            return

        if not status:

            messagebox.showerror(
                "Error",
                "Please select Status.",
                parent=window
            )

            return

        # ====================================================
        # DATE VALIDATION
        # ====================================================

        try:

            datetime.strptime(
                attendance_date,
                "%Y-%m-%d"
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Date",
                "Date must be in YYYY-MM-DD format.",
                parent=window
            )

            return

        # ====================================================
        # TIME VALIDATION
        # ====================================================

        if check_in:

            try:

                datetime.strptime(
                    check_in,
                    "%H:%M"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Check In",
                    "Check In must use HH:MM format.\n\n"
                    "Example: 09:30",
                    parent=window
                )

                return

        if check_out:

            try:

                datetime.strptime(
                    check_out,
                    "%H:%M"
                )

            except ValueError:

                messagebox.showerror(
                    "Invalid Check Out",
                    "Check Out must use HH:MM format.\n\n"
                    "Example: 18:00",
                    parent=window
                )

                return

        # ====================================================
        # STATUS VALIDATION
        # ====================================================

        if status == "Present":

            if not check_in:

                messagebox.showerror(
                    "Missing Check In",
                    "Please enter Check In time "
                    "for Present attendance.",
                    parent=window
                )

                return

            if not check_out:

                messagebox.showerror(
                    "Missing Check Out",
                    "Please enter Check Out time "
                    "for Present attendance.",
                    parent=window
                )

                return

        # ====================================================
        # ABSENT / LEAVE
        # ====================================================

        if status in (
            "Absent",
            "Leave"
        ):

            # Check-out should not be mandatory.
            # Empty values are allowed.
            pass

        # ====================================================
        # CHECK-IN / CHECK-OUT ORDER
        # ====================================================

        if check_in and check_out:

            try:

                in_time = datetime.strptime(
                    check_in,
                    "%H:%M"
                )

                out_time = datetime.strptime(
                    check_out,
                    "%H:%M"
                )

                if out_time < in_time:

                    messagebox.showerror(
                        "Invalid Time",
                        "Check Out cannot be earlier "
                        "than Check In.",
                        parent=window
                    )

                    return

            except ValueError:

                return

        # ====================================================
        # DUPLICATE CHECK
        # ====================================================

        records = load_attendance()

        for record in records:

            same_employee = (
                record.get(
                    "Employee ID",
                    ""
                ) == employee_id
            )

            same_date = (
                record.get(
                    "Date",
                    ""
                ) == attendance_date
            )

            if same_employee and same_date:

                messagebox.showerror(
                    "Duplicate Attendance",
                    (
                        "Attendance already exists "
                        "for this employee on this date."
                    ),
                    parent=window
                )

                return

        # ====================================================
        # NEW RECORD
        # ====================================================

        new_record = {
            "Employee ID": employee_id,
            "Employee Name": employee_name,
            "Date": attendance_date,
            "Check In": check_in,
            "Check Out": check_out,
            "Status": status
        }

        records.append(
            new_record
        )

        # ====================================================
        # SAVE
        # ====================================================

        if not save_attendance(
            records
        ):

            return

        # ====================================================
        # REFRESH
        # ====================================================

        refresh_attendance()

        # ====================================================
        # LOG
        # ========================================================

        log(
            "ADD ATTENDANCE",
            (
                f"Marked {status} for "
                f"{employee_id} - "
                f"{employee_name} "
                f"on {attendance_date}"
            )
        )

        # ====================================================
        # CLEAR
        # ====================================================

        clear_fields()

        messagebox.showinfo(
            "Success",
            (
                "Attendance marked successfully.\n\n"
                f"Employee: {employee_name}\n"
                f"Date: {attendance_date}\n"
                f"Status: {status}"
            ),
            parent=window
        )

    # ========================================================
    # DELETE ATTENDANCE
    # ========================================================

    def delete_attendance():

        selected = (
            attendance_tree.selection()
        )

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select an attendance record.",
                parent=window
            )

            return

        item = attendance_tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if len(values) < 3:

            return

        employee_id = str(
            values[0]
        )

        employee_name = str(
            values[1]
        )

        attendance_date = str(
            values[2]
        )

        confirm = messagebox.askyesno(
            "Delete Attendance",
            (
                "Are you sure you want to delete "
                "this attendance record?\n\n"
                f"Employee: {employee_name}\n"
                f"Date: {attendance_date}"
            ),
            parent=window
        )

        if not confirm:

            return

        records = load_attendance()

        new_records = [
            record
            for record in records
            if not (
                record.get(
                    "Employee ID",
                    ""
                ) == employee_id
                and record.get(
                    "Date",
                    ""
                ) == attendance_date
            )
        ]

        if len(new_records) == len(
            records
        ):

            messagebox.showinfo(
                "Not Found",
                (
                    "The selected attendance record "
                    "no longer exists."
                ),
                parent=window
            )

            refresh_attendance()

            return

        if not save_attendance(
            new_records
        ):

            return

        refresh_attendance()

        log(
            "DELETE ATTENDANCE",
            (
                f"Deleted attendance for "
                f"{employee_id} - "
                f"{employee_name} "
                f"on {attendance_date}"
            )
        )

        messagebox.showinfo(
            "Success",
            "Attendance deleted successfully.",
            parent=window
        )

    # ========================================================
    # SEARCH ATTENDANCE
    # ========================================================

    def search_attendance():

        search_text = (
            search_entry.get()
            .strip()
            .lower()
        )

        records = load_attendance()

        if not search_text:

            display_records(
                records
            )

            status_bar.config(
                text=(
                    f"Showing {len(records)} "
                    "attendance record(s)."
                )
            )

            return

        filtered_records = []

        for record in records:

            employee_id = str(
                record.get(
                    "Employee ID",
                    ""
                )
            ).lower()

            employee_name = str(
                record.get(
                    "Employee Name",
                    ""
                )
            ).lower()

            attendance_date = str(
                record.get(
                    "Date",
                    ""
                )
            ).lower()

            status = str(
                record.get(
                    "Status",
                    ""
                )
            ).lower()

            if (
                search_text in employee_id
                or search_text in employee_name
                or search_text in attendance_date
                or search_text in status
            ):

                filtered_records.append(
                    record
                )

        display_records(
            filtered_records
        )

        status_bar.config(
            text=(
                f"Found {len(filtered_records)} "
                "matching record(s)."
            )
        )

    # ========================================================
    # CLEAR SEARCH
    # ========================================================

    def clear_search():

        search_entry.delete(
            0,
            tk.END
        )

        refresh_attendance()

        search_entry.focus_set()

    # ========================================================
    # SHOW ALL
    # ========================================================

    def show_all():

        clear_search()

    # ========================================================
    # SELECT TABLE RECORD
    # ========================================================

    def load_selected_record(
        event=None
    ):

        selected = (
            attendance_tree.selection()
        )

        if not selected:

            return

        item = attendance_tree.item(
            selected[0]
        )

        values = item.get(
            "values",
            []
        )

        if len(values) < 6:

            return

        employee_id = str(
            values[0]
        )

        attendance_date = str(
            values[2]
        )

        check_in = str(
            values[3]
        )

        check_out = str(
            values[4]
        )

        status = str(
            values[5]
        )

        # ----------------------------------------------------
        # Employee
        # ----------------------------------------------------

        for employee in employee_list:

            if employee["id"] == employee_id:

                employee_combo.set(
                    f"{employee['id']} - "
                    f"{employee['name']}"
                )

                break

        # ----------------------------------------------------
        # Date
        # ----------------------------------------------------

        date_entry.delete(
            0,
            tk.END
        )

        date_entry.insert(
            0,
            attendance_date
        )

        # ----------------------------------------------------
        # Check In
        # ----------------------------------------------------

        checkin_entry.delete(
            0,
            tk.END
        )

        checkin_entry.insert(
            0,
            check_in
        )

        # ----------------------------------------------------
        # Check Out
        # ----------------------------------------------------

        checkout_entry.delete(
            0,
            tk.END
        )

        checkout_entry.insert(
            0,
            check_out
        )

        # ----------------------------------------------------
        # Status
        # ----------------------------------------------------

        status_combo.set(
            status
        )

        status_bar.config(
            text=(
                "Selected attendance record. "
                "Use Delete to remove it."
            )
        )

    # ========================================================
    # TITLE
    # ========================================================

    tk.Label(
        window,
        text="EMPLOYEE ATTENDANCE MANAGEMENT",
        font=("Arial", 24, "bold")
    ).pack(
        pady=(18, 5)
    )

    tk.Label(
        window,
        text="Admin Attendance Panel",
        font=("Arial", 11)
    ).pack(
        pady=(0, 12)
    )

    # ========================================================
    # SUMMARY
    # ========================================================

    summary_frame = tk.Frame(
        window
    )

    summary_frame.pack(
        fill=tk.X,
        padx=25
    )

    tk.Label(
        summary_frame,
        text="Total Attendance Records:",
        font=("Arial", 12, "bold")
    ).pack(
        side=tk.LEFT
    )

    total_label = tk.Label(
        summary_frame,
        text="0",
        font=("Arial", 14, "bold")
    )

    total_label.pack(
        side=tk.LEFT,
        padx=10
    )

    # ========================================================
    # FORM
    # ========================================================

    form_frame = tk.LabelFrame(
        window,
        text="Mark Attendance",
        font=("Arial", 12, "bold")
    )

    form_frame.pack(
        fill=tk.X,
        padx=25,
        pady=15
    )

    # ========================================================
    # EMPLOYEE
    # ========================================================

    tk.Label(
        form_frame,
        text="Employee"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10,
        sticky="e"
    )

    employee_values = [
        f"{employee['id']} - {employee['name']}"
        for employee in employee_list
    ]

    employee_combo = ttk.Combobox(
        form_frame,
        values=employee_values,
        state="readonly",
        width=34
    )

    employee_combo.grid(
        row=0,
        column=1,
        padx=10,
        pady=10,
        sticky="w"
    )

    employee_combo.bind(
        "<<ComboboxSelected>>",
        on_employee_selected
    )

    # ========================================================
    # DATE
    # ========================================================

    tk.Label(
        form_frame,
        text="Date"
    ).grid(
        row=0,
        column=2,
        padx=10,
        pady=10,
        sticky="e"
    )

    date_entry = tk.Entry(
        form_frame,
        width=18
    )

    date_entry.grid(
        row=0,
        column=3,
        padx=10,
        pady=10,
        sticky="w"
    )

    date_entry.insert(
        0,
        date.today().strftime(
            "%Y-%m-%d"
        )
    )

    tk.Button(
        form_frame,
        text="Today",
        command=set_default_date,
        width=8
    ).grid(
        row=0,
        column=4,
        padx=5
    )

    # ========================================================
    # CHECK IN
    # ========================================================

    tk.Label(
        form_frame,
        text="Check In"
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10,
        sticky="e"
    )

    checkin_entry = tk.Entry(
        form_frame,
        width=18
    )

    checkin_entry.grid(
        row=1,
        column=1,
        padx=10,
        pady=10,
        sticky="w"
    )

    tk.Button(
        form_frame,
        text="Now",
        command=lambda:
        set_current_time(
            checkin_entry
        ),
        width=8
    ).grid(
        row=1,
        column=2,
        padx=5
    )

    # ========================================================
    # CHECK OUT
    # ========================================================

    tk.Label(
        form_frame,
        text="Check Out"
    ).grid(
        row=1,
        column=3,
        padx=10,
        pady=10,
        sticky="e"
    )

    checkout_entry = tk.Entry(
        form_frame,
        width=18
    )

    checkout_entry.grid(
        row=1,
        column=4,
        padx=10,
        pady=10,
        sticky="w"
    )

    tk.Button(
        form_frame,
        text="Now",
        command=lambda:
        set_current_time(
            checkout_entry
        ),
        width=8
    ).grid(
        row=1,
        column=5,
        padx=5
    )

    # ========================================================
    # STATUS
    # ========================================================

    tk.Label(
        form_frame,
        text="Status"
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=10,
        sticky="e"
    )

    status_combo = ttk.Combobox(
        form_frame,
        values=[
            "Present",
            "Absent",
            "Leave"
        ],
        state="readonly",
        width=16
    )

    status_combo.grid(
        row=2,
        column=1,
        padx=10,
        pady=10,
        sticky="w"
    )

    status_combo.set(
        "Present"
    )

    # ========================================================
    # FORM BUTTONS
    # ========================================================

    form_button_frame = tk.Frame(
        window
    )

    form_button_frame.pack(
        pady=5
    )

    tk.Button(
        form_button_frame,
        text="Mark Attendance",
        command=add_attendance,
        width=18,
        height=2
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    tk.Button(
        form_button_frame,
        text="Clear",
        command=clear_fields,
        width=14,
        height=2
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    tk.Button(
        form_button_frame,
        text="Delete Record",
        command=delete_attendance,
        width=15,
        height=2
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    tk.Button(
        form_button_frame,
        text="Refresh",
        command=refresh_attendance,
        width=13,
        height=2
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    # ========================================================
    # SEARCH
    # ========================================================

    search_frame = tk.Frame(
        window
    )

    search_frame.pack(
        fill=tk.X,
        padx=25,
        pady=15
    )

    tk.Label(
        search_frame,
        text="Search:",
        font=("Arial", 11, "bold")
    ).pack(
        side=tk.LEFT
    )

    search_entry = tk.Entry(
        search_frame,
        width=35,
        font=("Arial", 11)
    )

    search_entry.pack(
        side=tk.LEFT,
        padx=8
    )

    tk.Button(
        search_frame,
        text="Search",
        command=search_attendance,
        width=12
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    tk.Button(
        search_frame,
        text="Show All",
        command=show_all,
        width=12
    ).pack(
        side=tk.LEFT,
        padx=5
    )

    # ========================================================
    # TABLE
    # ========================================================

    table_frame = tk.Frame(
        window
    )

    table_frame.pack(
        fill=tk.BOTH,
        expand=True,
        padx=25,
        pady=(0, 10)
    )

    columns = tuple(
        ATTENDANCE_HEADERS
    )

    attendance_tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        selectmode="browse"
    )

    widths = {
        "Employee ID": 110,
        "Employee Name": 220,
        "Date": 120,
        "Check In": 110,
        "Check Out": 110,
        "Status": 120
    }

    for column in columns:

        attendance_tree.heading(
            column,
            text=column
        )

        attendance_tree.column(
            column,
            width=widths.get(
                column,
                120
            ),
            anchor="center"
        )

    scrollbar_y = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=attendance_tree.yview
    )

    scrollbar_x = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=attendance_tree.xview
    )

    attendance_tree.configure(
        yscrollcommand=scrollbar_y.set,
        xscrollcommand=scrollbar_x.set
    )

    attendance_tree.pack(
        side=tk.LEFT,
        fill=tk.BOTH,
        expand=True
    )

    scrollbar_y.pack(
        side=tk.RIGHT,
        fill=tk.Y
    )

    scrollbar_x.pack(
        side=tk.BOTTOM,
        fill=tk.X
    )

    attendance_tree.bind(
        "<<TreeviewSelect>>",
        load_selected_record
    )

    # ========================================================
    # STATUS BAR
    # ========================================================

    status_bar = tk.Label(
        window,
        text="",
        anchor="w",
        font=("Arial", 10)
    )

    status_bar.pack(
        fill=tk.X,
        padx=25,
        pady=(0, 8)
    )

    # ========================================================
    # KEYBOARD SHORTCUTS
    # ========================================================

    window.bind(
        "<F5>",
        lambda event:
        refresh_attendance()
    )

    window.bind(
        "<Control-f>",
        lambda event: (
            search_entry.focus_set(),
            search_entry.select_range(
                0,
                tk.END
            )
        )
    )

    window.bind(
        "<Escape>",
        lambda event:
        clear_fields()
    )

    window.bind(
        "<Delete>",
        lambda event:
        delete_attendance()
    )

    window.bind(
        "<Control-s>",
        lambda event:
        add_attendance()
    )

    search_entry.bind(
        "<Return>",
        lambda event:
        search_attendance()
    )

    # ========================================================
    # INITIAL DATA
    # ========================================================

    refresh_attendance()

    if employee_list:

        employee_combo.focus_set()

    else:

        status_bar.config(
            text=(
                "No employees found. "
                "Please add employees first."
            )
        )

    # ========================================================
    # CLOSE WINDOW
    # ========================================================

    def close_window():

        try:

            if parent is not None:

                window.grab_release()

        except Exception:
            pass

        window.destroy()

    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )

    # ========================================================
    # STANDALONE MODE
    # ========================================================

    if parent is None:

        window.mainloop()

    return window


# ============================================================
# STANDALONE TEST MODE
# ============================================================

if __name__ == "__main__":

    open_attendance_window(
        parent=None,
        employees=None,
        username="admin",
        role="ADMIN"
    )