import pytest
from password_generator import generate_password


def test_default_password_length():
    assert len(generate_password()) == 16


def test_password_length_is_respected():
    assert len(generate_password(length=24)) == 24


def test_invalid_length_is_rejected():
    with pytest.raises(ValueError):
        generate_password(length=10)


def test_no_character_type_is_rejected():
    with pytest.raises(ValueError):
        generate_password(
            use_upper=False,
            use_lower=False,
            use_digits=False,
            use_symbols=False
        )


def test_selected_character_types_are_included():
    password = generate_password(length=16)
    assert any(c.isupper() for c in password)
    assert any(c.islower() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(not c.isalnum() for c in password)
