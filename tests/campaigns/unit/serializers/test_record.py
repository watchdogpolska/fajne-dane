from unittest import TestCase

from campaigns.models import Record, UserSource
from campaigns.serializers import RecordSerializer
from tests.campaigns.conftest import advanced_campaign_with_documents
from tests.conftest import user1


def basic_record() -> Record:
    campaign = advanced_campaign_with_documents()
    record = campaign.documents.first().document_queries.first().records.first()
    return record


class RecordSerializerTestCase(TestCase):
    def test_serialize(self):
        record = basic_record()
        serializer = RecordSerializer(record)
        source = record.source.to_child()

        self.assertEqual(
            serializer.data,
            {
                'id': record.id,
                'value': record.value,
                'probability': record.probability,
                'source': {
                    'id': source.id,
                    'name': source.name,
                    'type': source.type
                },
                'status': record.status
            }
        )

    def test_update(self):
        instance = basic_record()
        serializer = RecordSerializer(
            instance,
            data={
                'value': "tak",
                'probability': 0.2,
            },
            partial=True
        )
        serializer.is_valid()
        serializer.save()
        instance.refresh_from_db()

        self.assertEqual(instance.value, "tak")
        self.assertEqual(instance.probability, 0.2)

    def test_create(self):
        source, _ = UserSource.objects.get_or_create(user=user1())
        campaign = advanced_campaign_with_documents()
        document = campaign.documents.first()
        dq = document.document_queries.first()

        serializer = RecordSerializer(
            data={
                'value': "tak",
                'probability': 0.2,
                'parent': dq.id
            }
        )
        serializer.is_valid()
        record = serializer.save(source=source)

        self.assertIsInstance(record, Record)
