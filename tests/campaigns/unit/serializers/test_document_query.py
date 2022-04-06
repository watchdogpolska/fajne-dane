from django.test import TestCase

from campaigns.serializers import DocumentQuerySerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_document_query


class DocumentQuerySerializerTestCase(TestCase):

    def test_serialize(self):
        dq = basic_document_query()
        serializer = DocumentQuerySerializer(dq)

        self.assertEqual(
            serializer.data,
            {
                "id": dq.id,
                "query": {
                    "id": dq.query.id,
                    "order": 0,
                    "name": "question 1",
                    "data": {
                        "question": {
                            "name": "question",
                            "value": "What is it?",
                            "type": "str",
                            "widget": "label"
                        }
                    }
                },
                "status": "CREATED"
            }
        )

    def test_update(self):
        instance = basic_document_query()

        serializer = DocumentQuerySerializer(
            instance,
            data={
                "query_id": 1,
                "document_id": 1
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()


    def test_create(self):
        serializer = DocumentQuerySerializer(
            data={
                'status': "NONE",
                'query_id': 1,
                'document_queries': []
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()
