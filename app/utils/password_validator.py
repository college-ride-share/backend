import re

def validate_password(password: str) -> bool:
    """
    Validates a password based on the following criteria:
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    - Minimum length of 8 characters

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    # Define the validation criteria
    min_length = 8
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_number = bool(re.search(r'[0-9]', password))
    has_special_char = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    has_min_length = len(password) >= min_length

    # Return True only if all criteria are met
    return all([has_uppercase, has_lowercase, has_number, has_special_char, has_min_length])