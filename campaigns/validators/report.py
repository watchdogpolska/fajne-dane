def validate_report(csv: pd.DataFrame):
    return True


import json
import pandas as pd

schema = json.load(open("./tests/campaigns/test_data/campaign_schema_sample.json"))
df = pd.read_csv('./tests/campaigns/test_data/campaign_report_sample.csv', header=[0, 1])

data_fields = [f['name'] for f in schema['document']['data_fields']]
data_fields_columns = [('data_fields', f) for f in data_fields]

class DocumentSerializer:
    def from_data_frame_row(self):
        return



import json
import pandas as pd
from campaigns.validators.template.document_schema import DocumentSchema
from campaigns.parsers.data_frame_parser import DataFrameParser

raw_schema = json.load(open("./tests/campaigns/test_data/campaign_schema_sample.json"))
schema = DocumentSchema.from_json(raw_schema['document'])
df = pd.read_csv('./tests/campaigns/test_data/campaign_report_sample.csv', header=[0, 1])

DataFrameParser(schema).parse(df)
