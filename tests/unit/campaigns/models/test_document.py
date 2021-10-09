from django.test import TestCase

from campaigns.models import Document
from tests.unit.campaigns.models.conftest import basic_campaign, basic_file_source


class DocumentTestCase(TestCase):
    def test_creating(self):
        document = Document.objects.create(
            campaign=basic_campaign(),
            source=basic_file_source(),
            data={"institution_id": 1}
        )
        self.assertIsInstance(document, Document)
