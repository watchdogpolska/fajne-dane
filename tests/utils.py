import json
from pathlib import Path

import pandas as pd

def _get_test_data_path(directory: str, data_file: str) -> Path:
    return Path(__file__).resolve().parent / "test_data" / directory / data_file


def get_test_data(directory: str, data_file: str) -> str:
    return open(_get_test_data_path(directory, data_file)).read()


def get_json_test_data(directory: str, data_file: str) -> dict:
    return json.loads(get_test_data(directory, data_file))


def get_csv_data(directory: str, data_file: str) -> pd.DataFrame:
    return pd.read_csv(_get_test_data_path(directory, data_file))
