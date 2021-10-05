import json
from pathlib import Path


def get_test_data(directory: str, data_file: str) -> str:
    return open(Path(__file__).resolve().parent / "test_data" / directory / data_file).read()


def get_json_test_data(directory: str, data_file: str) -> dict:
    return json.loads(get_test_data(directory, data_file))
