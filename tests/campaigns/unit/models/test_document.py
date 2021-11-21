from django.test import TestCase

from campaigns.models import Document
from tests.campaigns.conftest import basic_campaign, basic_file_source


class DocumentTestCase(TestCase):
    def test_creating(self):
        campaign = basic_campaign()
        document = Document.objects.create(
            campaign=campaign,
            source=basic_file_source(campaign),
            data={"institution_id": 1}
        )
        self.assertIsInstance(document, Document)
