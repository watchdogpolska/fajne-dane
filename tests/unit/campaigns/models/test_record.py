from django.test import TestCase

from campaigns.models import Record
from tests.unit.campaigns.models.conftest import basic_query, basic_document, basic_user_source


class RecordTestCase(TestCase):
    def setUp(self):
        pass

    def test_creating(self):
        record = Record.objects.create(
            query=basic_query(),
            document=basic_document(),
            source=basic_user_source(),
            value="yes",
            probability=0.7
        )
        self.assertIsInstance(record, Record)
