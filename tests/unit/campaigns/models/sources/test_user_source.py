from django.test import TestCase

from campaigns.models import Source, UserSource, FileSource
from campaigns.models.sources.source import SourceTypes
from tests.unit.campaigns.conftest import user1


class UserSourceTestCase(TestCase):

    def test_creating(self):
        source = UserSource.objects.create(
            name="user's source",
            user=user1()
        )

        self.assertIsInstance(source, UserSource)
        self.assertIsInstance(source, Source)
        self.assertEqual(source.type, SourceTypes.USER)
