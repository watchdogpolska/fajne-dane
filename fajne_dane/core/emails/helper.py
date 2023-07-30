from dataclasses import dataclass
from webbrowser import get

from django.contrib.auth.models import User
from django.core.mail import send_mail

from fajne_dane.consts import Platform
from fajne_dane.settings import EMAIL_HOST_USER, PANEL_URL, API_URL
from typing import Text


def _send(email, subject, body):
    send_mail(subject, "", EMAIL_HOST_USER, [email], html_message=body)




def send_registration_email(user: User, token: Text, platform: Platform):
    if platform == Platform.API:
        url = f"{API_URL}/accounts/activate/?token={token.token}"
    else:
        url = f"{PANEL_URL}/authentication/activate/?token={token.token}"

    _send(
        user.email,
        'Aktywacja konta Fajne Dane API',
        f"""
            <p>Witaj {user.first_name}!</p>
            <p>Twój token aktywacyjny to: <b>{token.token}</b>.</p>
            <p>
                Aktywacje konta możesz wykonać ręcznie przy użyciu odpowiedniego endpointa, albo po prostu klikająć w poniższy link:<br/>
                <a href="{url}" target="_blank">
                    {url}
                </a>
            </p>
            <p>Powodzenia,<br/>Zespół Fajne Dane</p>
        """
    )


def send_reset_password_email(user: User, token: Text, platform: Platform):
    if platform == Platform.API:
        url = f"{API_URL}/accounts/change-password/?token={token.token}"
    else:
        url = f"{PANEL_URL}/authentication/change-password/?token={token.token}"

    _send(
        user.email,
        'Reset hasła Fajne Dane API',
        f"""
            <p>Witaj {user.first_name}!</p>
            <p>Twój token restartujący to: <b>{token.token}</b>.</p>
            <p>
                Reset hasła możesz wykonać ręcznie przy użyciu odpowiedniego endpointa, albo po prostu klikająć w poniższy link:<br/>
                <a href="{url}" target="_blank">
                    {url}
                </a>
            </p>
            <p>Powodzenia,<br/>Zespół Fajne Dane</p>
        """
    )
