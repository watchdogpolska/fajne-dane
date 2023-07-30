import json
from datetime import datetime
from pathlib import Path
from typing import List, Union, Text

import pandas as pd


def _get_test_data_path(directory: Text, data_file: Text) -> Path:
    return Path(__file__).resolve().parent / "test_data" / directory / data_file


def get_test_file(directory: Text, data_file: Text, mode='r'):
    return open(_get_test_data_path(directory, data_file), mode=mode)


def get_test_data(directory: Text, data_file: Text) -> Text:
    return  get_test_file(directory, data_file).read()


def get_json_test_data(directory: Text, data_file: Text) -> dict:
    return json.loads(get_test_data(directory, data_file))


def get_csv_data(directory: Text, data_file: Text, header: Union[int, List[int]] = 0) -> pd.DataFrame:
    return pd.read_csv(_get_test_data_path(directory, data_file), header=header)


def serialize_date(date: datetime) -> Text:
    return date.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
