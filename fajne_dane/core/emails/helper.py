from dataclasses import dataclass

from django.contrib.auth.models import User
from django.core.mail import send_mail
from fajne_dane.settings import EMAIL_HOST_USER


def _send(email, subject, body):
    send_mail(subject, "", EMAIL_HOST_USER, [email], html_message=body)


def send_registration_email(user: User, token: str):
    _send(
        user.email,
        'Aktywacja konta SpaceCalc',
        f"""
            <p>Witaj {user.username}!</p>
            <p>{token}</p>
            <p>Powodzenia,<br/>Zespół Fajne Dane</p>
        """
    )


def send_reset_password_email(user: User, token: str):
    _send(
        user.email,
        'Reset hasła Fajne Dane',
        f"""
            <p>Cześć {user.username}!</p>
            <p>{token}</p>
            <p>Pozdrawiamy,<br/>Zespół Fajne Dane</p>
        """
    )
