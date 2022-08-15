from django.test import TestCase

from campaigns.models import UserSource
from campaigns.models.consts import DocumentStatus
from campaigns.serializers import DocumentFullSerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_document
from tests.conftest import user1
from tests.utils import serialize_date


class DocumentFullSerializerTestCase(TestCase):

    def test_serialize(self):
        document = basic_document()
        serializer = DocumentFullSerializer(document)

        source = document.source.to_child()
        self.assertEqual(
            serializer.data,
            {
                'id': document.id,
                'data': document.data,
                'status': document.status.name,
                'institution': {
                    'id': document.institution.id,
                    'key': document.institution.key,
                    'name': document.institution.name
                },
                'source': {
                    'id': source.id,
                    'name': source.name,
                    'type': source.type
                },
                'created': serialize_date(document.created),
                'document_queries': []
            }
        )

    def test_update(self):
        instance = basic_document()

        serializer = DocumentFullSerializer(
            instance,
            data={"data": {"institution_id": "123"}}
        )
        serializer.is_valid()
        serializer.save()

        instance.refresh_from_db()
        self.assertEqual(instance.data, {"institution_id": "123"})

    def test_create(self):
        source, _ = UserSource.objects.get_or_create(user=user1())
        serializer = DocumentFullSerializer(
            data={"data": {"institution_id": "123"}},
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()
