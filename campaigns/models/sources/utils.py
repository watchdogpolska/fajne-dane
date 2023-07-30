import io

import pandas as pd
from django.core.files.base import File


def load_data_frame(input_file: File):
    with input_file.open('rb') as file:
        content = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(content), header=[0, 1])
        return df

