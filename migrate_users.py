import json
import os
import shutil
from datetime import datetime

from auth import hash_password


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

USERS_FILE = os.path.join(
    BASE_DIR,
    "users.json"
)

BACKUP_FOLDER = os.path.join(
    BASE_DIR,
    "backups"
)


# ============================================================
# CREATE BACKUP
# ============================================================

def create_users_backup():

    os.makedirs(
        BACKUP_FOLDER,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = os.path.join(
        BACKUP_FOLDER,
        f"users_backup_{timestamp}.json"
    )

    shutil.copy2(
        USERS_FILE,
        backup_file
    )

    return backup_file


# ============================================================
# NORMALIZE ROLE
# ============================================================

def normalize_role(role):

    role = str(
        role or ""
    ).strip().upper()

    if role in (
        "ADMIN",
        "ADMINISTRATOR"
    ):
        return "ADMIN"

    return "EMPLOYEE"


# ============================================================
# CHECK HASH
# ============================================================

def is_hashed(password):

    return str(
        password
    ).startswith(
        "pbkdf2_sha256$"
    )


# ============================================================
# MIGRATE USER
# ============================================================

def migrate_user(user):

    if not isinstance(
        user,
        dict
    ):
        return False

    # --------------------------------------------------------
    # GET PASSWORD
    # --------------------------------------------------------

    password = user.get(
        "password"
    )

    password_hash = user.get(
        "password_hash"
    )

    # --------------------------------------------------------
    # ALREADY USING password_hash
    # --------------------------------------------------------

    if password_hash:

        password_hash = str(
            password_hash
        )

        # Already correctly hashed
        if is_hashed(
            password_hash
        ):

            user["password_hash"] = password_hash

            user.pop(
                "password",
                None
            )

        else:

            # Unexpected password_hash value.
            # Don't destroy it automatically.
            print(
                "WARNING: Invalid password_hash found."
            )

            return False

    # --------------------------------------------------------
    # OLD password FIELD
    # --------------------------------------------------------

    elif password is not None:

        password = str(
            password
        )

        if not password:

            print(
                "WARNING: Empty password found."
            )

            return False

        # If old password field already contains
        # a PBKDF2 hash, simply move it.
        if is_hashed(
            password
        ):

            user["password_hash"] = password

        else:

            # Convert plain-text password
            # into secure PBKDF2 hash.
            user["password_hash"] = hash_password(
                password
            )

        # Remove old password field.
        user.pop(
            "password",
            None
        )

    else:

        print(
            "WARNING: User has no password."
        )

        return False

    # --------------------------------------------------------
    # NORMALIZE ROLE
    # --------------------------------------------------------

    user["role"] = normalize_role(
        user.get(
            "role",
            "EMPLOYEE"
        )
    )

    return True


# ============================================================
# MIGRATE USERS
# ============================================================

def migrate_users():

    print("=" * 60)
    print("EMPLOYEE MANAGEMENT SYSTEM")
    print("USER SECURITY MIGRATION")
    print("=" * 60)

    # --------------------------------------------------------
    # CHECK FILE
    # --------------------------------------------------------

    if not os.path.exists(
        USERS_FILE
    ):

        print()
        print(
            "ERROR: users.json was not found."
        )

        print(
            "Expected location:"
        )

        print(
            USERS_FILE
        )

        return

    # --------------------------------------------------------
    # LOAD JSON
    # --------------------------------------------------------

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            users = json.load(
                file
            )

    except Exception as error:

        print()
        print(
            "ERROR: Could not read users.json."
        )

        print(
            str(error)
        )

        return

    # --------------------------------------------------------
    # BACKUP FIRST
    # --------------------------------------------------------

    try:

        backup_file = create_users_backup()

        print()
        print(
            "Backup created successfully:"
        )

        print(
            backup_file
        )

    except Exception as error:

        print()
        print(
            "ERROR: Could not create backup."
        )

        print(
            str(error)
        )

        print()
        print(
            "Migration cancelled for safety."
        )

        return

    # --------------------------------------------------------
    # MIGRATION COUNTERS
    # --------------------------------------------------------

    total_users = 0

    migrated_users = 0

    already_secure = 0

    failed_users = 0

    # ========================================================
    # FORMAT 1
    #
    # {
    #     "admin": {
    #         "password": "...",
    #         "role": "admin"
    #     }
    # }
    # ========================================================

    if isinstance(
        users,
        dict
    ):

        # ----------------------------------------------------
        # NORMAL USER DICTIONARY
        # ----------------------------------------------------

        for username, user in list(
            users.items()
        ):

            # Skip special "users" list
            if username == "users":

                continue

            if not isinstance(
                user,
                dict
            ):

                continue

            total_users += 1

            was_hashed = bool(
                user.get(
                    "password_hash"
                )
                and is_hashed(
                    user.get(
                        "password_hash"
                    )
                )
            )

            old_password = user.get(
                "password"
            )

            success = migrate_user(
                user
            )

            if success:

                if was_hashed:

                    already_secure += 1

                else:

                    migrated_users += 1

                print(
                    f"OK: {username}"
                )

            else:

                failed_users += 1

                print(
                    f"FAILED: {username}"
                )

        # ----------------------------------------------------
        # DICTIONARY WITH USERS LIST
        #
        # {
        #     "users": [
        #         {...}
        #     ]
        # }
        # ----------------------------------------------------

        user_list = users.get(
            "users"
        )

        if isinstance(
            user_list,
            list
        ):

            for user in user_list:

                if not isinstance(
                    user,
                    dict
                ):

                    continue

                total_users += 1

                username = str(
                    user.get(
                        "username",
                        "Unknown"
                    )
                )

                was_hashed = bool(
                    user.get(
                        "password_hash"
                    )
                    and is_hashed(
                        user.get(
                            "password_hash"
                        )
                    )
                )

                success = migrate_user(
                    user
                )

                if success:

                    if was_hashed:

                        already_secure += 1

                    else:

                        migrated_users += 1

                    print(
                        f"OK: {username}"
                    )

                else:

                    failed_users += 1

                    print(
                        f"FAILED: {username}"
                    )

    # ========================================================
    # FORMAT 2
    #
    # [
    #     {
    #         "username": "admin",
    #         "password": "...",
    #         "role": "ADMIN"
    #     }
    # ]
    # ========================================================

    elif isinstance(
        users,
        list
    ):

        for user in users:

            if not isinstance(
                user,
                dict
            ):

                continue

            total_users += 1

            username = str(
                user.get(
                    "username",
                    "Unknown"
                )
            )

            was_hashed = bool(
                user.get(
                    "password_hash"
                )
                and is_hashed(
                    user.get(
                        "password_hash"
                    )
                )
            )

            success = migrate_user(
                user
            )

            if success:

                if was_hashed:

                    already_secure += 1

                else:

                    migrated_users += 1

                print(
                    f"OK: {username}"
                )

            else:

                failed_users += 1

                print(
                    f"FAILED: {username}"
                )

    else:

        print()
        print(
            "ERROR: Unsupported users.json format."
        )

        return

    # ========================================================
    # SAVE
    # ========================================================

    try:

        with open(
            USERS_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                users,
                file,
                indent=4
            )

    except Exception as error:

        print()
        print(
            "ERROR: Could not save users.json."
        )

        print(
            str(error)
        )

        print()
        print(
            "Your original users.json is still "
            "available in the backups folder."
        )

        return

    # ========================================================
    # RESULT
    # ========================================================

    print()
    print("=" * 60)
    print("MIGRATION COMPLETED")
    print("=" * 60)

    print(
        f"Total users:       {total_users}"
    )

    print(
        f"Newly secured:     {migrated_users}"
    )

    print(
        f"Already secure:    {already_secure}"
    )

    print(
        f"Failed:            {failed_users}"
    )

    print()
    print(
        "All successful users now use:"
    )

    print(
        "PBKDF2-HMAC-SHA256"
    )

    print(
        "600,000 iterations"
    )

    print()
    print(
        "Backup location:"
    )

    print(
        backup_file
    )

    print()
    print(
        "You can now close this window."
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    migrate_users()

    input(
        "\nPress ENTER to exit..."
    )