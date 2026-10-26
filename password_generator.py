
import secrets
import string


def generate_password(length=16, use_upper=True,
                      use_lower=True, use_digits=True,
                      use_symbols=True):
    """Generate a cryptographically random password of 16–24 characters."""

    if not isinstance(length, int) or isinstance(length, bool):
        raise ValueError("Length must be an integer.")

    if not 16 <= length <= 24:
        raise ValueError("Password length must be between 16 and 24.")

    pools = []

    if use_upper:
        pools.append(string.ascii_uppercase)
    if use_lower:
        pools.append(string.ascii_lowercase)
    if use_digits:
        pools.append(string.digits)
    if use_symbols:
        pools.append("!@#$%^&*()-_=+?")

    if not pools:
        raise ValueError("Select at least one character type.")

    if length < len(pools):
        raise ValueError("Length is too short for selected character types.")

    # Ensure at least one character from every selected type.
    password_chars = [secrets.choice(pool) for pool in pools]
    all_chars = "".join(pools)

    password_chars.extend(
        secrets.choice(all_chars)
        for _ in range(length - len(password_chars))
    )

    # Securely shuffle the characters.
    secrets.SystemRandom().shuffle(password_chars)

    return "".join(password_chars)
