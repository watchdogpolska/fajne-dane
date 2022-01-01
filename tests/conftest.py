from typing import Dict

import pandas as pd

from tests.utils import get_json_test_data, get_csv_data, get_test_file
from users.models.user import User


def user1(is_active=False, is_staff=False) -> User:
    user = User.objects.filter(email="test_user@test.com").first()
    if not user:
        user = User.objects.create_user(
            email="test_user@test.com",
            password="password",
            first_name="Test",
            last_name="User"
        )
    user.is_active = is_active
    user.is_staff = is_staff
    user.save()
    return user


def basic_campaign_template() -> Dict:
    return get_json_test_data("campaigns", "basic_campaign-template.json")


def advanced_campaign_template() -> Dict:
    return get_json_test_data("campaigns", "advanced_campaign-template.json")


def basic_campaign_dataset() -> pd.DataFrame:
    return get_csv_data("campaigns", "basic_campaign-dataset.csv")


def basic_campaign_dataset_wrong_no_prob() -> pd.DataFrame:
    return get_csv_data("campaigns", "basic_campaign_wrong_no_prob-dataset.csv")


def basic_campaign_documents_file(mode='r'):
    return get_test_file("campaigns", "basic_campaign-dataset.csv", mode=mode)


def advanced_campaign_dataset() -> pd.DataFrame:
    return get_csv_data("campaigns", "advanced_campaign-dataset.csv")


def wrong_advanced_campaign_dataset() -> pd.DataFrame:
    return get_csv_data("campaigns", "advanced_campaign_wrong-dataset.csv")


def wrong_advanced_campaign_documents_file(mode='r'):
    return get_test_file("campaigns", "advanced_campaign_wrong-dataset.csv", mode=mode)
