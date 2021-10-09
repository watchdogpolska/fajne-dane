from django.test import TestCase

from campaigns.models import Source, FileSource
from campaigns.models.sources.source import SourceTypes


class FileSourceTestCase(TestCase):

    def test_creating(self):
        source = FileSource.objects.create(
            name="file source",
            description="this is a file"
        )

        self.assertIsInstance(source, FileSource)
        self.assertIsInstance(source, Source)
        self.assertEqual(source.type, SourceTypes.FILE)
