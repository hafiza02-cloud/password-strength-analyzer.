
import hashlib
import requests


def check_password_breach(password):
    """
    Check a password using the Have I Been Pwned range API.
    Only the first five SHA-1 hash characters are sent.
    The raw password is never sent.
    """

    if not isinstance(password, str) or not password:
        raise ValueError("Enter a password to check.")

    sha1_hash = hashlib.sha1(
        password.encode("utf-8")
    ).hexdigest().upper()

    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"

    response = requests.get(
        url,
        headers={"Add-Padding": "true"},
        timeout=10
    )
    response.raise_for_status()

    for line in response.text.splitlines():
        parts = line.split(":")

        if len(parts) == 2 and parts[0].upper() == suffix:
            return {
                "breached": True,
                "count": int(parts[1])
            }

    return {"breached": False, "count": 0}
