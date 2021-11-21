from django.test import TestCase

from campaigns.serializers.sources import SourceSerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_file_source, basic_campaign


class SourceSerializerTestCase(TestCase):
    def test_serialize(self):
        source = basic_file_source(basic_campaign())
        serializer = SourceSerializer(source)

        self.assertEqual(
            serializer.data,
            {
                'id': source.id,
                'name': source.name
            }
        )

    def test_update(self):
        instance = basic_file_source(basic_campaign())
        serializer = SourceSerializer(
            instance,
            data={
                'name': "other",
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()

    def test_create(self):
        serializer = SourceSerializer(
            data={
                'name': "other",
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()
