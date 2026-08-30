import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import date, datetime


ATTENDANCE_FILE = "attendance.csv"


# -----------------------------
# Load attendance
# -----------------------------
def load_attendance():
    records = []

    if os.path.exists(ATTENDANCE_FILE):
        with open(
            ATTENDANCE_FILE,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                records.append(row)

    return records


# -----------------------------
# Save attendance
# -----------------------------
def save_attendance(records):

    fieldnames = [
        "Employee ID",
        "Employee Name",
        "Date",
        "Check In",
        "Check Out",
        "Status"
    ]

    with open(
        ATTENDANCE_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(records)


# -----------------------------
# Display records
# -----------------------------
def display_records(records):

    for item in attendance_tree.get_children():
        attendance_tree.delete(item)

    for record in records:

        attendance_tree.insert(
            "",
            tk.END,
            values=(
                record.get("Employee ID", ""),
                record.get("Employee Name", ""),
                record.get("Date", ""),
                record.get("Check In", ""),
                record.get("Check Out", ""),
                record.get("Status", "")
            )
        )


# -----------------------------
# Refresh attendance
# -----------------------------
def refresh_attendance():

    records = load_attendance()

    display_records(records)

    total_label.config(
        text=str(len(records))
    )


# -----------------------------
# Add attendance
# -----------------------------
def add_attendance():

    employee_id = id_entry.get().strip()
    employee_name = name_entry.get().strip()
    attendance_date = date_entry.get().strip()
    check_in = checkin_entry.get().strip()
    check_out = checkout_entry.get().strip()
    status = status_combo.get()

    if not employee_id:
        messagebox.showerror(
            "Error",
            "Please enter Employee ID."
        )
        return

    if not employee_name:
        messagebox.showerror(
            "Error",
            "Please enter Employee Name."
        )
        return

    if not attendance_date:
        messagebox.showerror(
            "Error",
            "Please enter Date."
        )
        return

    if not check_in:
        messagebox.showerror(
            "Error",
            "Please enter Check In time."
        )
        return

    if status == "Present" and not check_out:
        messagebox.showerror(
            "Error",
            "Please enter Check Out time."
        )
        return

    # Validate date
    try:
        datetime.strptime(
            attendance_date,
            "%Y-%m-%d"
        )
    except ValueError:
        messagebox.showerror(
            "Error",
            "Date must be in YYYY-MM-DD format."
        )
        return

    records = load_attendance()

    # Prevent duplicate attendance
    for record in records:

        if (
            record.get("Employee ID") == employee_id
            and record.get("Date") == attendance_date
        ):

            messagebox.showerror(
                "Duplicate",
                "Attendance already exists for this employee on this date."
            )

            return

    records.append(
        {
            "Employee ID": employee_id,
            "Employee Name": employee_name,
            "Date": attendance_date,
            "Check In": check_in,
            "Check Out": check_out,
            "Status": status
        }
    )

    save_attendance(records)

    refresh_attendance()

    clear_fields()

    messagebox.showinfo(
        "Success",
        "Attendance added successfully."
    )


# -----------------------------
# Delete attendance
# -----------------------------
def delete_attendance():

    selected = attendance_tree.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select an attendance record."
        )

        return

    item = attendance_tree.item(
        selected[0]
    )

    values = item["values"]

    employee_id = str(values[0])
    attendance_date = str(values[2])

    confirm = messagebox.askyesno(
        "Delete Attendance",
        "Are you sure you want to delete this attendance record?"
    )

    if not confirm:
        return

    records = load_attendance()

    records = [
        record
        for record in records
        if not (
            record.get("Employee ID") == employee_id
            and record.get("Date") == attendance_date
        )
    ]

    save_attendance(records)

    refresh_attendance()

    messagebox.showinfo(
        "Success",
        "Attendance deleted successfully."
    )


# -----------------------------
# Search attendance
# -----------------------------
def search_attendance():

    search_text = search_entry.get().strip().lower()

    records = load_attendance()

    filtered_records = []

    for record in records:

        employee_id = record.get(
            "Employee ID",
            ""
        ).lower()

        employee_name = record.get(
            "Employee Name",
            ""
        ).lower()

        attendance_date = record.get(
            "Date",
            ""
        ).lower()

        if (
            search_text in employee_id
            or search_text in employee_name
            or search_text in attendance_date
        ):

            filtered_records.append(record)

    display_records(filtered_records)


# -----------------------------
# Clear fields
# -----------------------------
def clear_fields():

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    checkin_entry.delete(0, tk.END)
    checkout_entry.delete(0, tk.END)

    date_entry.delete(0, tk.END)
    date_entry.insert(
        0,
        date.today().strftime("%Y-%m-%d")
    )

    status_combo.set("Present")


# -----------------------------
# Main window
# -----------------------------
root = tk.Tk()

root.title(
    "Employee Attendance System"
)

root.geometry(
    "1100x700"
)

root.resizable(
    True,
    True
)


# -----------------------------
# Heading
# -----------------------------
tk.Label(
    root,
    text="Employee Attendance System",
    font=("Arial", 24, "bold")
).pack(pady=15)


# -----------------------------
# Total records
# -----------------------------
summary_frame = tk.Frame(root)

summary_frame.pack(
    fill=tk.X,
    padx=20
)

tk.Label(
    summary_frame,
    text="Total Attendance Records:",
    font=("Arial", 12, "bold")
).pack(side=tk.LEFT)

total_label = tk.Label(
    summary_frame,
    text="0",
    font=("Arial", 14, "bold")
)

total_label.pack(
    side=tk.LEFT,
    padx=10
)


# -----------------------------
# Attendance form
# -----------------------------
form_frame = tk.LabelFrame(
    root,
    text="Attendance Details",
    font=("Arial", 12, "bold")
)

form_frame.pack(
    fill=tk.X,
    padx=20,
    pady=15
)


# Employee ID
tk.Label(
    form_frame,
    text="Employee ID"
).grid(
    row=0,
    column=0,
    padx=10,
    pady=10
)

id_entry = tk.Entry(
    form_frame,
    width=20
)

id_entry.grid(
    row=0,
    column=1,
    padx=10
)


# Employee Name
tk.Label(
    form_frame,
    text="Employee Name"
).grid(
    row=0,
    column=2,
    padx=10
)

name_entry = tk.Entry(
    form_frame,
    width=20
)

name_entry.grid(
    row=0,
    column=3,
    padx=10
)


# Date
tk.Label(
    form_frame,
    text="Date"
).grid(
    row=1,
    column=0,
    padx=10,
    pady=10
)

date_entry = tk.Entry(
    form_frame,
    width=20
)

date_entry.grid(
    row=1,
    column=1,
    padx=10
)

date_entry.insert(
    0,
    date.today().strftime("%Y-%m-%d")
)


# Check In
tk.Label(
    form_frame,
    text="Check In"
).grid(
    row=1,
    column=2,
    padx=10
)

checkin_entry = tk.Entry(
    form_frame,
    width=20
)

checkin_entry.grid(
    row=1,
    column=3,
    padx=10
)


# Check Out
tk.Label(
    form_frame,
    text="Check Out"
).grid(
    row=2,
    column=0,
    padx=10,
    pady=10
)

checkout_entry = tk.Entry(
    form_frame,
    width=20
)

checkout_entry.grid(
    row=2,
    column=1,
    padx=10
)


# Status
tk.Label(
    form_frame,
    text="Status"
).grid(
    row=2,
    column=2,
    padx=10
)

status_combo = ttk.Combobox(
    form_frame,
    values=[
        "Present",
        "Absent",
        "Leave"
    ],
    state="readonly",
    width=18
)

status_combo.grid(
    row=2,
    column=3,
    padx=10
)

status_combo.set("Present")


# -----------------------------
# Buttons
# -----------------------------
form_button_frame = tk.Frame(root)

form_button_frame.pack(pady=5)


tk.Button(
    form_button_frame,
    text="Add Attendance",
    command=add_attendance,
    width=18,
    height=2,
    bg="green",
    fg="white"
).pack(
    side=tk.LEFT,
    padx=5
)


tk.Button(
    form_button_frame,
    text="Clear",
    command=clear_fields,
    width=15,
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
    height=2,
    bg="red",
    fg="white"
).pack(
    side=tk.LEFT,
    padx=5
)


tk.Button(
    form_button_frame,
    text="Refresh",
    command=refresh_attendance,
    width=15,
    height=2
).pack(
    side=tk.LEFT,
    padx=5
)


# -----------------------------
# Search
# -----------------------------
search_frame = tk.Frame(root)

search_frame.pack(
    pady=15
)

tk.Label(
    search_frame,
    text="Search Employee / Date:",
    font=("Arial", 11)
).pack(
    side=tk.LEFT,
    padx=5
)

search_entry = tk.Entry(
    search_frame,
    width=30,
    font=("Arial", 11)
)

search_entry.pack(
    side=tk.LEFT,
    padx=5
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
    command=refresh_attendance,
    width=12
).pack(
    side=tk.LEFT,
    padx=5
)


# -----------------------------
# Attendance table
# -----------------------------
table_frame = tk.Frame(root)

table_frame.pack(
    fill=tk.BOTH,
    expand=True,
    padx=20,
    pady=10
)


columns = (
    "Employee ID",
    "Employee Name",
    "Date",
    "Check In",
    "Check Out",
    "Status"
)


attendance_tree = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


for column in columns:

    attendance_tree.heading(
        column,
        text=column
    )


attendance_tree.column(
    "Employee ID",
    width=120
)

attendance_tree.column(
    "Employee Name",
    width=200
)

attendance_tree.column(
    "Date",
    width=130
)

attendance_tree.column(
    "Check In",
    width=120
)

attendance_tree.column(
    "Check Out",
    width=120
)

attendance_tree.column(
    "Status",
    width=120
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=attendance_tree.yview
)

attendance_tree.configure(
    yscrollcommand=scrollbar.set
)


attendance_tree.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


# -----------------------------
# Start
# -----------------------------
refresh_attendance()

root.mainloop()