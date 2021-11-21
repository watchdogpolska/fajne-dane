from django.test import TestCase

from campaigns.models import Source, FileSource, UserSource
from campaigns.models.sources.source import SourceTypes
from tests.campaigns.conftest import basic_file_source, basic_user_source, basic_campaign


class SourceTestCase(TestCase):
    def setUp(self):
        pass

    def test_creating(self):
        source = Source.objects.create(
            name="test"
        )

        self.assertIsInstance(source, Source)
        self.assertEqual(source.type, SourceTypes.NONE)

    def test_to_child_none(self):
        source = Source.objects.create(name="test")
        with self.assertRaises(TypeError):
            source.to_child()

    def test_to_child_file(self):
        basic_file_source(basic_campaign())
        source = Source.objects.first()
        file_source = source.to_child()

        self.assertEqual(source.id, file_source.id)
        self.assertNotIsInstance(source, FileSource)
        self.assertIsInstance(file_source, FileSource)

    def test_to_child_user(self):
        basic_user_source()
        source = Source.objects.first()
        user_source = source.to_child()

        self.assertEqual(source.id, user_source.id)
        self.assertNotIsInstance(source, UserSource)
        self.assertIsInstance(user_source, UserSource)
