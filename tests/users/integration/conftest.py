from typing import Dict


def registration_payload() -> Dict:
    return {
        "username": "username",
        "email": "test@email.com",
        "first_name": "User",
        "last_name": "Test",
        "password": "testpass123",
        "password_confirmation": "testpass123",
    }

def registration_payload_passwords_not_match() -> Dict:
    payload = registration_payload()
    payload['password_confirmation'] = "otherpassword"
    return payload


def registration_payload_used_username() -> Dict:
    payload = registration_payload()
    payload['username'] = "test_user"
    return payload


def registration_payload_used_email() -> Dict:
    payload = registration_payload()
    payload['email'] = "test_user@test.com"
    return payload


