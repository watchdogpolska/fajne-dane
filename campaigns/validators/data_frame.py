from dataclasses import dataclass

import pandas as pd
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from campaigns.models import Campaign


@dataclass
class DataFrameValidator:
    campaign: Campaign
    
    def _validate_document_fields_columns(self, df: pd.DataFrame):
        errors = []
        for f in self.campaign.document_fields.all():
            key = ('data_fields', f.name)
            if key not in df.columns:
                errors.append(
                    ValidationError(
                        _("Document field column: '%(value)s' not found in provided data frame."),
                        code='missing-column',
                        params={'value': f.name}
                    )
                )
        if errors:
            raise ValidationError({"data": errors})

    def _validate_record_fields_columns(self, df: pd.DataFrame):
        errors = []
        for query in self.campaign.queries_objects:
            # check query name
            if query.name not in df.columns:
                errors.append(
                    ValidationError(
                        _("Query column: '%(value)s' not found in provided data frame."),
                        code='missing-column',
                        params={'value': query.name}
                    )
                )

            # check query output field
            # TODO: Let's add a check for query data fields
            for field_name in [
                query.output_field.name, f"{query.output_field.name}__probability"
            ]:
                key = (query.name, field_name)
                if key not in df.columns:
                    errors.append(
                        ValidationError(
                            _("Query column: '%(value)s' not found in provided data frame."),
                            code='missing-column',
                            params={'value': key}
                        )
                    )

        if errors:
            raise ValidationError({"data": errors})

    def validate(self, df: pd.DataFrame):
        errors = []
        try:
            self._validate_document_fields_columns(df)
        except ValidationError as e:
            errors.extend(e.error_dict['data'])

        try:
            self._validate_record_fields_columns(df)
        except ValidationError as e:
            errors.extend(e.error_dict['data'])

        if errors:
            raise ValidationError({"data": errors})
