from django.test import TestCase

from campaigns.models import OutputField
from campaigns.serializers import OutputFieldSerializer
from fajne_dane.core.exceptions import NotSupported


def basic_output_field() -> OutputField:
    return OutputField.objects.create(
        name="output",
        widget="TextField",
        answers=['yes', 'no'],
        metadata={},
        type="str",
        validation=True,
        default_answer=0
    )


class OutputFieldSerializerTestCase(TestCase):
    def test_serialize(self):
        output_field = basic_output_field()
        serializer = OutputFieldSerializer(output_field)
        self.assertEqual(
            serializer.data,
            {
                'id': output_field.id,
                'name': output_field.name,
                'metadata': output_field.metadata,
                'widget': output_field.widget,
                'answers': output_field.answers,
                'type': output_field.type,
                'validation': output_field.validation,
                'default_answer': output_field.default_answer
            }
        )

    def test_update(self):
        instance = basic_output_field()

        serializer = OutputFieldSerializer(
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
        serializer = OutputFieldSerializer(
            data={
                'name': 'output',
                'widget': 'TextField',
                'type': 'str',
                'answers': ['yes', 'no'],
                'validation': True,
                'default_answer': 0
            }
        )
        serializer.is_valid()
        serializer.save()

        output_field = OutputField.objects.first()
        self.assertIsInstance(output_field, OutputField)
