from argon2 import PasswordHasher

from argon2.exceptions import (
    VerifyMismatchError,
    VerificationError
)
password_hasher = PasswordHasher()
def hash_password(password):

    return password_hasher.hash(
        password
    )

def verify_password(
    password,
    password_hash
):
    try:
        return password_hasher.verify(
            password_hash,
            password
        )
    except (
        VerifyMismatchError,
        VerificationError
    ):
        return False

def validate_password_strength(password):

    if len(password) < 8:
        return False

    has_uppercase = any(
        character.isupper()
        for character in password
    )

    has_lowercase = any(
        character.islower()
        for character in password
    )

    has_digit = any(
        character.isdigit()
        for character in password
    )

    has_special = any(
        not character.isalnum()
        for character in password
    )

    return (
        has_uppercase
        and has_lowercase
        and has_digit
        and has_special
    )