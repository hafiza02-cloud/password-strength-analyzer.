
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from password_analyzer import analyze_password


def test_empty_password():
    result = analyze_password("")
    assert result["score"] == 0
    assert result["risk"] == "High"


def test_common_password_is_flagged():
    result = analyze_password("password123")
    assert result["score"] <= 49
    assert result["checks"]["Not a listed common password"] is False


def test_keyboard_pattern_is_flagged():
    result = analyze_password("qwerty987!ABC")
    assert result["checks"]["No common keyboard patterns"] is False


def test_sequence_is_flagged():
    result = analyze_password("abcdef123!XYZ")
    assert result["checks"]["No obvious sequences"] is False


def test_repeated_characters_are_flagged():
    result = analyze_password("AAAA1111!!!!")
    assert result["checks"]["No long repeated characters"] is False


def test_result_has_expected_fields():
    result = analyze_password("Fictional-Example-92!Tiger")
    assert 0 <= result["score"] <= 100
    assert result["strength"] in {"Weak", "Fair", "Good", "Strong"}
    assert result["risk"] in {"Low", "Medium", "High"}
    assert isinstance(result["recommendations"], list)
