from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase

from campaigns.models import Campaign, Query, OutputField
from campaigns.models.dto import RecordDTO
from tests.campaigns.conftest import basic_query, basic_campaign


class QueryTestCase(TestCase):
    def setUp(self):
        basic_campaign()
        OutputField.objects.create(
            name="test_field",
            widget="text_label",
            answers=["yes", "no"],
            type="str",
            validation=False,
            default_answer=0
        )

    def test_creating(self):
        query = Query.objects.create(
            campaign=Campaign.objects.first(),
            order=0,
            name="question 1",
            data={
                "question": {
                    "name": "question",
                    "value": "What is it?",
                    "type": "str",
                    "widget": "label"
                }
            },
            output_field=OutputField.objects.first()
        )
        self.assertIsInstance(query, Query)

    def test_creating_without_output_filed(self):
        with self.assertRaises(IntegrityError):
            Query.objects.create(
                campaign=Campaign.objects.first(),
                order=0,
                name="question 1",
                data={
                    "question": {
                        "name": "question",
                        "value": "What is it?",
                        "type": "str",
                        "widget": "label"
                    }
                }
            )
            
    def test_validating(self):
        with patch.object(OutputField, 'validate', return_value=None) as mock_method:
            query = basic_query()
            query.validate_record(RecordDTO(
                value=1,
                probability=1
            ))
            self.assertEqual(mock_method.call_count, 1)
