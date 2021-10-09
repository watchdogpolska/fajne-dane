from typing import Dict

from django.contrib.auth.models import User

from tests.utils import get_json_test_data


def basic_campaign_template() -> Dict:
    return get_json_test_data("campaigns", "basic_campaign-template.json")


def user1() -> User:
    user, _ = User.objects.get_or_create(
        username="test_user",
        email="test_user@test.com",
        password="password"
    )
    return user
