from django.test import TestCase

from campaigns.models import DocumentDataField
from campaigns.serializers import DocumentDataFieldCreateSerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_campaign


def basic_document_data_field() -> DocumentDataField:
    return DocumentDataField.objects.create(
        campaign=basic_campaign(),
        name="institution_id",
        widget="TestLabel",
        type="str"
    )


class DocumentDataFieldCreateSerializerTestCase(TestCase):
    def test_serialize(self):
        data_field = basic_document_data_field()
        serializer = DocumentDataFieldCreateSerializer(data_field)
        self.assertEqual(
            serializer.data,
            {
                'id': data_field.id,
                'name': data_field.name,
                'widget': data_field.widget,
                'type': data_field.type,
            }
        )

    def test_update(self):
        instance = basic_document_data_field()

        serializer = DocumentDataFieldCreateSerializer(
            instance,
            data={
                "name": "institution",
                "widget": "TextField",
                "type": "str"
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()

    def test_create(self):
        campaign = basic_campaign()
        serializer = DocumentDataFieldCreateSerializer(
            data={
                "name": "institution",
                "widget": "TextLabel",
                "type": "str"
            }
        )
        serializer.is_valid()
        serializer.save(campaign=campaign)

        data_field = campaign.document_fields.first()
        self.assertEqual(campaign.document_fields.count(), 1)
        self.assertIsInstance(data_field, DocumentDataField)
