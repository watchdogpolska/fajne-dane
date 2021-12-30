import io

import pandas as pd
from django.db.models.fields.files import FieldFile


def load_data_frame(input_file: FieldFile):
    with input_file.open('rb') as file:
        content = file.read().decode('utf-8')
        df = pd.read_csv(io.StringIO(content), header=[0, 1])
        return df

