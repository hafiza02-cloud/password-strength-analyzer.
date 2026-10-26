
import re
import string

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678",
    "123456789", "qwerty", "qwerty123", "admin",
    "admin123", "letmein", "welcome", "iloveyou",
    "abc123", "111111", "000000"
}

KEYBOARD_PATTERNS = [
    "qwerty", "asdfgh", "zxcvbn",
    "123456", "654321"
]

SEQUENCES = [
    "abcdef", "bcdefg", "cdefgh",
    "123456", "234567", "345678",
    "987654", "876543", "zyxwvu"
]


def analyze_password(password):
    """Analyze password characteristics without storing the input."""

    if not isinstance(password, str):
        raise TypeError("Password must be a string.")

    if not password:
        return {
            "score": 0,
            "strength": "Weak",
            "risk": "High",
            "checks": {},
            "recommendations": ["Enter a password to begin analysis."]
        }

    length = len(password)
    lower = any(c.islower() for c in password)
    upper = any(c.isupper() for c in password)
    digit = any(c.isdigit() for c in password)
    symbol = any(not c.isalnum() for c in password)

    common = password.casefold() in COMMON_PASSWORDS

    repeated = bool(re.search(r"(.)\1{3,}", password))

    normalized = password.casefold()
    sequence = any(item in normalized for item in SEQUENCES)

    keyboard = any(
        pattern in normalized for pattern in KEYBOARD_PATTERNS
    )

    checks = {
        "At least 12 characters": length >= 12,
        "At least 16 characters": length >= 16,
        "Contains uppercase letters": upper,
        "Contains lowercase letters": lower,
        "Contains numbers": digit,
        "Contains symbols": symbol,
        "Not a listed common password": not common,
        "No long repeated characters": not repeated,
        "No obvious sequences": not sequence,
        "No common keyboard patterns": not keyboard
    }

    # Length contributes up to 40 points.
    if length >= 24:
        score = 40
    elif length >= 16:
        score = 35
    elif length >= 12:
        score = 25
    elif length >= 8:
        score = 15
    else:
        score = 5

    # Character variety contributes up to 40 points.
    score += 10 * sum([lower, upper, digit, symbol])

    # Extra points for length.
    if length >= 20:
        score += 5
    if length >= 24:
        score += 5

    # Penalties for predictable patterns.
    if common:
        score -= 50
    if repeated:
        score -= 15
    if sequence:
        score -= 15
    if keyboard:
        score -= 15

    score = max(0, min(100, score))

    # Predictable passwords cannot receive a high score.
    if common or repeated or sequence or keyboard:
        score = min(score, 49)

    if score < 30:
        strength = "Weak"
    elif score < 50:
        strength = "Fair"
    elif score < 75:
        strength = "Good"
    else:
        strength = "Strong"

    if strength in ("Weak", "Fair"):
        risk = "High"
    elif strength == "Good":
        risk = "Medium"
    else:
        risk = "Low"

    recommendations = []

    if length < 16:
        recommendations.append(
            "Aim for at least 16 characters or a long, "
            "unpredictable passphrase."
        )
    if not upper or not lower:
        recommendations.append(
            "Consider mixing uppercase and lowercase letters."
        )
    if not digit:
        recommendations.append("Consider including numbers.")
    if not symbol:
        recommendations.append("Consider including symbols.")
    if common:
        recommendations.append(
            "Avoid common passwords and easily guessed choices."
        )
    if repeated:
        recommendations.append(
            "Avoid long runs of repeated characters."
        )
    if sequence:
        recommendations.append(
            "Avoid predictable ascending or descending sequences."
        )
    if keyboard:
        recommendations.append(
            "Avoid familiar keyboard patterns."
        )

    if not recommendations:
        recommendations.append(
            "No obvious weaknesses were detected by these checks. "
            "Use a unique password for every account."
        )

    return {
        "score": score,
        "strength": strength,
        "risk": risk,
        "checks": checks,
        "recommendations": recommendations
    }
