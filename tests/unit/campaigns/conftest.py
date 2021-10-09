from typing import Dict

import pandas as pd
from django.contrib.auth.models import User

from tests.utils import get_json_test_data, get_csv_data


def basic_campaign_template() -> Dict:
    return get_json_test_data("campaigns", "basic_campaign-template.json")


def advanced_campaign_template() -> Dict:
    return get_json_test_data("campaigns", "advanced_campaign-template.json")


def advanced_campaign_dataset() -> pd.DataFrame:
    return get_csv_data("campaigns", "advanced_campaign-dataset.csv")



def user1() -> User:
    user, _ = User.objects.get_or_create(
        username="test_user",
        email="test_user@test.com",
        password="password"
    )
    return user
