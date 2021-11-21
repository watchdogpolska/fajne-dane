from django.test import TestCase

from campaigns.models import UserSource
from campaigns.serializers import DocumentSerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_document
from tests.conftest import user1


class DocumentSerializerTestCase(TestCase):

    def test_serialize(self):
        document = basic_document()
        serializer = DocumentSerializer(document)

        source = document.source.to_child()
        self.assertEqual(
            serializer.data,
            {
                'id': document.id,
                'data': document.data,
                'status': 'NONE',
                'source': {
                    'id': source.id,
                    'name': source.name,
                    'description': source.description,
                    'file': None
                }
            }
        )

    def test_update(self):
        instance = basic_document()

        serializer = DocumentSerializer(
            instance,
            data={"data": {"institution_id": "123"}}
        )
        serializer.is_valid()
        serializer.save()

        instance.refresh_from_db()
        self.assertEqual(instance.data, {"institution_id": "123"})

    def test_create(self):
        source, _ = UserSource.objects.get_or_create(user=user1())
        serializer = DocumentSerializer(
            data={"data": {"institution_id": "123"}},
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()
