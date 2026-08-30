import hashlib
import secrets
import hmac


# ============================================================
# SECURITY SETTINGS
# ============================================================

ALGORITHM = "sha256"

ITERATIONS = 600000

SALT_LENGTH = 32

KEY_LENGTH = 32


# ============================================================
# HASH PASSWORD
# ============================================================

def hash_password(password):
    """
    Convert a plain-text password into a secure
    PBKDF2-HMAC-SHA256 password hash.
    """

    password = str(password)

    salt = secrets.token_bytes(
        SALT_LENGTH
    )

    password_hash = hashlib.pbkdf2_hmac(
        ALGORITHM,
        password.encode("utf-8"),
        salt,
        ITERATIONS,
        dklen=KEY_LENGTH
    )

    return (
        "pbkdf2_sha256$"
        + str(ITERATIONS)
        + "$"
        + salt.hex()
        + "$"
        + password_hash.hex()
    )


# ============================================================
# VERIFY PASSWORD
# ============================================================

def verify_password(
    password,
    stored_hash
):
    """
    Verify a password against a PBKDF2 hash.

    Returns:
        True  -> password is correct
        False -> password is incorrect
    """

    try:

        parts = str(
            stored_hash
        ).split("$")

        if len(parts) != 4:
            return False

        algorithm = parts[0]

        iterations = int(
            parts[1]
        )

        salt = bytes.fromhex(
            parts[2]
        )

        expected_hash = bytes.fromhex(
            parts[3]
        )

        if algorithm != "pbkdf2_sha256":
            return False

        calculated_hash = hashlib.pbkdf2_hmac(
            ALGORITHM,
            str(password).encode("utf-8"),
            salt,
            iterations,
            dklen=len(expected_hash)
        )

        return hmac.compare_digest(
            calculated_hash,
            expected_hash
        )

    except Exception:
        return False