import json
import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox
import hashlib
import secrets
import hmac
import time


# ============================================================
# FILE PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

USERS_FILE = os.path.join(
    BASE_DIR,
    "users.json"
)

GUI_FILE = os.path.join(
    BASE_DIR,
    "gui.py"
)


# ============================================================
# SECURITY SETTINGS
# ============================================================

HASH_ALGORITHM = "sha256"

PBKDF2_ITERATIONS = 600000

SALT_LENGTH = 32

HASH_LENGTH = 32

MAX_LOGIN_ATTEMPTS = 5

LOCKOUT_SECONDS = 30


# ============================================================
# LOGIN SECURITY STATE
# ============================================================

failed_attempts = 0

locked_until = 0


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    """
    Create a secure PBKDF2 password hash.

    Stored format:

        pbkdf2_sha256$iterations$salt$hash
    """

    password = str(password)

    salt = secrets.token_bytes(
        SALT_LENGTH
    )

    password_hash = hashlib.pbkdf2_hmac(
        HASH_ALGORITHM,
        password.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
        dklen=HASH_LENGTH
    )

    return (
        "pbkdf2_sha256$"
        + str(PBKDF2_ITERATIONS)
        + "$"
        + salt.hex()
        + "$"
        + password_hash.hex()
    )


# ============================================================
# VERIFY HASHED PASSWORD
# ============================================================

def verify_password(
    password,
    stored_password
):
    """
    Verify a PBKDF2 password.

    Returns:

        True  -> correct password
        False -> incorrect password
    """

    try:

        parts = str(
            stored_password
        ).split("$")

        if len(parts) != 4:
            return False

        algorithm = parts[0]

        iterations = int(
            parts[1]
        )

        salt_hex = parts[2]

        stored_hash_hex = parts[3]

        if algorithm != "pbkdf2_sha256":
            return False

        salt = bytes.fromhex(
            salt_hex
        )

        stored_hash = bytes.fromhex(
            stored_hash_hex
        )

        calculated_hash = hashlib.pbkdf2_hmac(
            HASH_ALGORITHM,
            str(password).encode("utf-8"),
            salt,
            iterations,
            dklen=len(stored_hash)
        )

        return hmac.compare_digest(
            calculated_hash,
            stored_hash
        )

    except Exception:
        return False


# ============================================================
# CHECK IF PASSWORD IS HASHED
# ============================================================

def is_password_hashed(password):
    """
    Detect whether a stored password uses
    our PBKDF2 format.
    """

    if not isinstance(
        password,
        str
    ):
        return False

    return password.startswith(
        "pbkdf2_sha256$"
    )


# ============================================================
# LOAD USERS
# ============================================================

def load_users():

    if not os.path.exists(
        USERS_FILE
    ):

        messagebox.showerror(
            "Error",
            "users.json file not found.\n\n"
            "Make sure users.json is inside:\n"
            + BASE_DIR
        )

        return None

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        return data

    except json.JSONDecodeError:

        messagebox.showerror(
            "Error",
            "users.json contains invalid JSON."
        )

        return None

    except Exception as error:

        messagebox.showerror(
            "Error",
            "Could not read users.json:\n\n"
            + str(error)
        )

        return None


# ============================================================
# SAVE USERS
# ============================================================

def save_users(users):

    temp_file = USERS_FILE + ".tmp"

    try:

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                users,
                file,
                indent=4
            )

        os.replace(
            temp_file,
            USERS_FILE
        )

        return True

    except Exception as error:

        try:

            if os.path.exists(
                temp_file
            ):
                os.remove(
                    temp_file
                )

        except Exception:
            pass

        messagebox.showerror(
            "Error",
            "Could not save users.json:\n\n"
            + str(error)
        )

        return False


# ============================================================
# NORMALIZE ROLE
# ============================================================

def normalize_role(role):

    role = str(
        role or "EMPLOYEE"
    ).strip().upper()

    if role not in [
        "ADMIN",
        "EMPLOYEE"
    ]:

        role = "EMPLOYEE"

    return role


# ============================================================
# PASSWORD MATCHING
# ============================================================

def password_matches(
    entered_password,
    stored_password
):
    """
    Verify the entered password.

    Supports:

    1. PBKDF2 hashed passwords
    2. Old plain-text passwords

    Plain-text support is retained only for
    compatibility with older user records.
    """

    stored_password = str(
        stored_password
    )

    # --------------------------------------------------------
    # HASHED PASSWORD
    # --------------------------------------------------------

    if is_password_hashed(
        stored_password
    ):

        return verify_password(
            entered_password,
            stored_password
        )

    # --------------------------------------------------------
    # OLD PLAIN-TEXT PASSWORD
    # --------------------------------------------------------

    return hmac.compare_digest(
        str(entered_password),
        stored_password
    )


# ============================================================
# MIGRATE OLD PASSWORD
# ============================================================

def migrate_password(
    users,
    username,
    old_password
):
    """
    Convert an old plain-text password into
    PBKDF2 after successful login.
    """

    changed = False

    # ========================================================
    # NORMAL DICTIONARY FORMAT
    # ========================================================

    if isinstance(
        users,
        dict
    ):

        user = users.get(
            username
        )

        if isinstance(
            user,
            dict
        ):

            stored_password = str(
                user.get(
                    "password",
                    ""
                )
            )

            if (
                stored_password
                and not is_password_hashed(
                    stored_password
                )
            ):

                user["password_hash"] = hash_password(
                    old_password
                )

                user.pop(
                    "password",
                    None
                )

                changed = True

        # ====================================================
        # DICTIONARY WITH USERS LIST
        # ====================================================

        user_list = users.get(
            "users"
        )

        if isinstance(
            user_list,
            list
        ):

            for item in user_list:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                item_username = str(
                    item.get(
                        "username",
                        ""
                    )
                ).strip()

                if item_username != username:
                    continue

                stored_password = str(
                    item.get(
                        "password",
                        ""
                    )
                )

                if (
                    stored_password
                    and not is_password_hashed(
                        stored_password
                    )
                ):

                    item["password_hash"] = hash_password(
                        old_password
                    )

                    item.pop(
                        "password",
                        None
                    )

                    changed = True

                break

    # ========================================================
    # LIST FORMAT
    # ========================================================

    elif isinstance(
        users,
        list
    ):

        for item in users:

            if not isinstance(
                item,
                dict
            ):
                continue

            item_username = str(
                item.get(
                    "username",
                    ""
                )
            ).strip()

            if item_username != username:
                continue

            stored_password = str(
                item.get(
                    "password",
                    ""
                )
            )

            if (
                stored_password
                and not is_password_hashed(
                    stored_password
                )
            ):

                item["password_hash"] = hash_password(
                    old_password
                )

                item.pop(
                    "password",
                    None
                )

                changed = True

            break

    if changed:

        save_users(
            users
        )


# ============================================================
# FIND USER
# ============================================================

def find_user(
    users,
    username
):
    """
    Find user information from supported
    users.json formats.

    Returns:

        {
            "password": "...",
            "role": "ADMIN"
        }

    or None.
    """

    # ========================================================
    # DICTIONARY FORMAT
    # ========================================================

    if isinstance(
        users,
        dict
    ):

        # ----------------------------------------------------
        # Direct username key
        # ----------------------------------------------------

        user = users.get(
            username
        )

        if isinstance(
            user,
            dict
        ):

            return {
                "password": str(
                    user.get(
                        "password_hash",
                        user.get(
                            "password",
                            ""
                        )
                    )
                ),
                "role": normalize_role(
                    user.get(
                        "role",
                        "EMPLOYEE"
                    )
                )
            }

        # ----------------------------------------------------
        # users list inside dictionary
        # ----------------------------------------------------

        user_list = users.get(
            "users"
        )

        if isinstance(
            user_list,
            list
        ):

            for item in user_list:

                if not isinstance(
                    item,
                    dict
                ):
                    continue

                item_username = str(
                    item.get(
                        "username",
                        ""
                    )
                ).strip()

                if item_username == username:

                    return {
                        "password": str(
                            item.get(
                                "password_hash",
                                item.get(
                                    "password",
                                    ""
                                )
                            )
                        ),
                        "role": normalize_role(
                            item.get(
                                "role",
                                "EMPLOYEE"
                            )
                        )
                    }

    # ========================================================
    # LIST FORMAT
    # ========================================================

    if isinstance(
        users,
        list
    ):

        for item in users:

            if not isinstance(
                item,
                dict
            ):
                continue

            item_username = str(
                item.get(
                    "username",
                    ""
                )
            ).strip()

            if item_username == username:

                return {
                    "password": str(
                        item.get(
                            "password_hash",
                            item.get(
                                "password",
                                ""
                            )
                        )
                    ),
                    "role": normalize_role(
                        item.get(
                            "role",
                            "EMPLOYEE"
                        )
                    )
                }

    return None


# ============================================================
# CHECK LOGIN
# ============================================================

def check_login(
    username,
    password
):

    global failed_attempts
    global locked_until

    # ========================================================
    # CHECK LOCKOUT
    # ========================================================

    current_time = time.time()

    if current_time < locked_until:

        remaining = int(
            locked_until - current_time
        ) + 1

        messagebox.showwarning(
            "Login Temporarily Locked",
            "Too many failed login attempts.\n\n"
            f"Please wait {remaining} seconds."
        )

        return None

    # ========================================================
    # LOAD USERS
    # ========================================================

    users = load_users()

    if users is None:
        return None

    username = str(
        username
    ).strip()

    password = str(
        password
    )

    # ========================================================
    # FIND USER
    # ========================================================

    user = find_user(
        users,
        username
    )

    if user is None:

        failed_attempts += 1

        if failed_attempts >= MAX_LOGIN_ATTEMPTS:

            locked_until = (
                time.time()
                + LOCKOUT_SECONDS
            )

            failed_attempts = 0

            messagebox.showwarning(
                "Account Temporarily Locked",
                "Too many failed login attempts.\n\n"
                f"Login is locked for "
                f"{LOCKOUT_SECONDS} seconds."
            )

        return None

    stored_password = user.get(
        "password",
        ""
    )

    # ========================================================
    # VERIFY PASSWORD
    # ========================================================

    if not password_matches(
        password,
        stored_password
    ):

        failed_attempts += 1

        if failed_attempts >= MAX_LOGIN_ATTEMPTS:

            locked_until = (
                time.time()
                + LOCKOUT_SECONDS
            )

            failed_attempts = 0

            messagebox.showwarning(
                "Account Temporarily Locked",
                "Too many failed login attempts.\n\n"
                f"Login is locked for "
                f"{LOCKOUT_SECONDS} seconds."
            )

        return None

    # ========================================================
    # LOGIN SUCCESS
    # ========================================================

    failed_attempts = 0

    locked_until = 0

    # ========================================================
    # MIGRATE OLD PASSWORD IF NECESSARY
    # ========================================================

    if not is_password_hashed(
        stored_password
    ):

        migrate_password(
            users,
            username,
            password
        )

    return normalize_role(
        user.get(
            "role",
            "EMPLOYEE"
        )
    )


# ============================================================
# OPEN GUI
# ============================================================

def open_gui(
    username,
    role
):

    if not os.path.exists(
        GUI_FILE
    ):

        messagebox.showerror(
            "Error",
            "gui.py file not found."
        )

        return

    try:

        subprocess.Popen(
            [
                sys.executable,
                GUI_FILE,
                username,
                role
            ],
            cwd=BASE_DIR
        )

        root.destroy()

    except Exception as error:

        messagebox.showerror(
            "Error",
            "Could not start Employee Management System:\n\n"
            + str(error)
        )


# ============================================================
# LOGIN
# ============================================================

def login():

    username = (
        username_entry
        .get()
        .strip()
    )

    password = password_entry.get()

    # ========================================================
    # VALIDATION
    # ========================================================

    if not username:

        messagebox.showwarning(
            "Login",
            "Please enter your username."
        )

        username_entry.focus()

        return

    if not password:

        messagebox.showwarning(
            "Login",
            "Please enter your password."
        )

        password_entry.focus()

        return

    # ========================================================
    # CHECK LOGIN
    # ========================================================

    role = check_login(
        username,
        password
    )

    if role is None:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password."
        )

        password_entry.delete(
            0,
            tk.END
        )

        password_entry.focus()

        return

    # ========================================================
    # LOGIN SUCCESS
    # ========================================================

    messagebox.showinfo(
        "Login Successful",
        f"Welcome {username}!\n\n"
        f"Role: {role}"
    )

    open_gui(
        username,
        role
    )


# ============================================================
# SHOW / HIDE PASSWORD
# ============================================================

def toggle_password():

    if password_entry.cget(
        "show"
    ) == "*":

        password_entry.config(
            show=""
        )

        show_button.config(
            text="Hide"
        )

    else:

        password_entry.config(
            show="*"
        )

        show_button.config(
            text="Show"
        )


# ============================================================
# EXIT APPLICATION
# ============================================================

def exit_application():

    if messagebox.askyesno(
        "Exit",
        "Are you sure you want to exit?"
    ):

        root.destroy()


# ============================================================
# LOGIN WINDOW
# ============================================================

root = tk.Tk()

root.title(
    "Employee Management System - Login"
)

root.geometry(
    "500x400"
)

root.resizable(
    False,
    False
)


# ============================================================
# TITLE
# ============================================================

title_label = tk.Label(
    root,
    text="EMPLOYEE MANAGEMENT SYSTEM",
    font=("Arial", 20, "bold")
)

title_label.pack(
    pady=35
)


# ============================================================
# LOGIN FRAME
# ============================================================

login_frame = tk.Frame(
    root
)

login_frame.pack(
    pady=10
)


# ============================================================
# USERNAME
# ============================================================

username_label = tk.Label(
    login_frame,
    text="Username:",
    font=("Arial", 12)
)

username_label.grid(
    row=0,
    column=0,
    padx=10,
    pady=12,
    sticky="e"
)


username_entry = tk.Entry(
    login_frame,
    width=28,
    font=("Arial", 12)
)

username_entry.grid(
    row=0,
    column=1,
    padx=10,
    pady=12
)


# ============================================================
# PASSWORD
# ============================================================

password_label = tk.Label(
    login_frame,
    text="Password:",
    font=("Arial", 12)
)

password_label.grid(
    row=1,
    column=0,
    padx=10,
    pady=12,
    sticky="e"
)


password_entry = tk.Entry(
    login_frame,
    width=28,
    font=("Arial", 12),
    show="*"
)

password_entry.grid(
    row=1,
    column=1,
    padx=10,
    pady=12
)


# ============================================================
# SHOW PASSWORD BUTTON
# ============================================================

show_button = tk.Button(
    login_frame,
    text="Show",
    width=8,
    command=toggle_password
)

show_button.grid(
    row=1,
    column=2,
    padx=5
)


# ============================================================
# LOGIN BUTTON
# ============================================================

login_button = tk.Button(
    root,
    text="LOGIN",
    width=18,
    height=2,
    font=("Arial", 12, "bold"),
    command=login
)

login_button.pack(
    pady=25
)


# ============================================================
# ENTER KEY
# ============================================================

root.bind(
    "<Return>",
    lambda event: login()
)


# ============================================================
# ESCAPE KEY
# ============================================================

root.bind(
    "<Escape>",
    lambda event: exit_application()
)


# ============================================================
# FOCUS USERNAME
# ============================================================

username_entry.focus()


# ============================================================
# START LOGIN
# ============================================================

root.mainloop()
