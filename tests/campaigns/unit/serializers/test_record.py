from unittest import TestCase

from campaigns.models import Record, UserSource
from campaigns.serializers import RecordSerializer
from tests.campaigns.conftest import advanced_campaign_with_documents
from tests.conftest import user1


def basic_records() -> Record:
    campaign = advanced_campaign_with_documents()
    record = campaign.documents.first().records.first()
    return record


class RecordSerializerTestCase(TestCase):
    def test_serialize(self):
        record = basic_records()
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
                    'source': source.source,
                    'description': source.description,
                    'file': None
                },
                'status': record.status
            }
        )

    def test_update(self):
        instance = basic_records()
        serializer = RecordSerializer(
            instance,
            data={
                'value': "tak",
                'probability': 0.2,
                'query': instance.query.id
            }
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
        query = campaign.queries.first()

        serializer = RecordSerializer(
            data={
                'value': "tak",
                'probability': 0.2,
                'query': query.id
            }
        )
        serializer.is_valid()
        record = serializer.save(document=document, source=source)

        self.assertIsInstance(record, Record)
