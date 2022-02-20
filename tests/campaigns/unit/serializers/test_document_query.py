from django.test import TestCase

from campaigns.models.consts import DocumentQueryStatus
from campaigns.serializers import DocumentQuerySerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_document_query
from tests.utils import serialize_date


class DocumentQuerySerializerTestCase(TestCase):

    def test_serialize(self):
        dq = basic_document_query()
        serializer = DocumentQuerySerializer(dq)

        self.assertEqual(
            serializer.data,
            {
                'id': dq.id,
                'status': dq.status.name,
                'query': {

                },
                'created': serialize_date(dq.created),
                'document_queries': []
            }
        )

    def test_update(self):
        instance = basic_document_query()

        serializer = DocumentQuerySerializer(
            instance,
            status=DocumentQueryStatus.CREATED,
            query_id=1,
            document_id=1
        )
        serializer.is_valid()
        serializer.save()

        instance.refresh_from_db()
        self.assertEqual(instance.data, {"institution_id": "123"})

    def test_create(self):
        serializer = DocumentQuerySerializer(
            status=DocumentQueryStatus.CREATED,
            query_id=1,
            document_id=1
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()
