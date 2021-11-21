from django.test import TestCase
from rest_framework.exceptions import ValidationError

from campaigns.models import Query, OutputField
from campaigns.serializers import QueryCreateSerializer, QuerySerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_query, basic_campaign


class QueryCreateSerializerTestCase(TestCase):
    def test_serialize(self):
        query = basic_query()
        serializer = QueryCreateSerializer(query)
        self.assertEqual(
            serializer.data,
            {
                'id': query.id,
                'order': query.order,
                'name': query.name,
                'data': query.data,
                'output_field': {
                    'id': query.output_field.id,
                    'name': query.output_field.name,
                    'widget': query.output_field.widget,
                    'answers': query.output_field.answers,
                    'metadata': query.output_field.metadata,
                    'type': query.output_field.type,
                    'validation': query.output_field.validation,
                    'default_answer': query.output_field.default_answer
                }
            }
        )

    def test_update(self):
        instance = basic_query()

        serializer = QueryCreateSerializer(
            instance,
            data={
                'order': 1,
                'name': 'Question 1',
                'data': {
                    'name': "question",
                    'value': "What is it?",
                    'type': 'str',
                    'widget': 'TextLabel'
                },
                'output_field': {
                    'name': 'answer',
                    'widget': 'TextField',
                    'answers': ['yes', 'no'],
                    'metadata': {},
                    'type': 'str',
                    'validation': True,
                    'default_answer': 0
                }
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()

    def test_create(self):
        campaign = basic_campaign()
        serializer = QueryCreateSerializer(
            data={
                'order': 1,
                'name': 'Question 1',
                'data': {
                    'name': "question",
                    'value': "What is it?",
                    'type': 'str',
                    'widget': 'TextLabel'
                },
                'output_field': {
                    'name': 'answer',
                    'widget': 'TextField',
                    'answers': ['yes', 'no'],
                    'metadata': {},
                    'type': 'str',
                    'validation': True,
                    'default_answer': 0
                }
            }
        )
        serializer.is_valid()
        serializer.save(campaign=campaign)

        query = Query.objects.first()
        self.assertEqual(campaign.queries.count(), 1)
        self.assertIsInstance(query, Query)
        self.assertIsInstance(query.output_field, OutputField)

    def test_create_wrong_output_field(self):
        serializer = QueryCreateSerializer(
            data={
                'order': 1,
                'name': 'Question 1',
                'data': {
                    'name': "question",
                    'value': "What is it?",
                    'type': 'str',
                    'widget': 'TextLabel'
                },
                'output_field': {
                    'widget': 'TextField',
                    'answers': ['yes', 'no'],
                    'metadata': {},
                    'type': 'str',
                    'validation': True,
                    'default_answer': 0
                }
            }
        )

        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)


class QuerySerializerTestCase(TestCase):
    def test_serialize(self):
        query = basic_query()
        serializer = QuerySerializer(query)
        self.assertEqual(
            serializer.data,
            {
                'id': query.id,
                'order': query.order,
                'name': query.name,
                'data': query.data,
                'output_field': {
                    'id': query.output_field.id,
                    'name': query.output_field.name,
                    'widget': query.output_field.widget,
                    'answers': query.output_field.answers,
                    'metadata': query.output_field.metadata,
                    'type': query.output_field.type,
                    'validation': query.output_field.validation,
                    'default_answer': query.output_field.default_answer
                }
            }
        )

    def test_update(self):
        instance = basic_query()

        serializer = QuerySerializer(
            instance,
            data={
                'order': 1,
                'name': 'Question 1',
                'data': {
                    'name': "question",
                    'value': "What is it?",
                    'type': 'str',
                    'widget': 'TextLabel'
                }
            }
        )
        serializer.is_valid()
        serializer.save(campaign=basic_campaign())

        instance.refresh_from_db()
        self.assertEqual(instance.name, "Question 1")

    def test_create(self):
        serializer = QuerySerializer(
            data={
                'order': 1,
                'name': 'Question 1',
                'data': {
                    'name': "question",
                    'value': "What is it?",
                    'type': 'str',
                    'widget': 'TextLabel'
                }
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save(campaign=basic_campaign())
