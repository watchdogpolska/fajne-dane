from django.test import TestCase

from campaigns.serializers.sources import UserSourceSerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_user_source


class UserSourceSerializerTestCase(TestCase):
    def test_serialize(self):
        source = basic_user_source()
        serializer = UserSourceSerializer(source)

        self.assertEqual(
            serializer.data,
            {
                'id': source.id,
                'name': source.name,
                'user': {
                    'id': source.user.id,
                    'first_name': source.user.first_name,
                    'last_name': source.user.last_name,
                    'email': source.user.email
                }
            }
        )

    def test_update(self):
        instance = basic_user_source()

        serializer = UserSourceSerializer(
            instance,
            data={
                'name': "other",
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()

    def test_create(self):
        serializer = UserSourceSerializer(
            data={
                'name': "other",
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()
