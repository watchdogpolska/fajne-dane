from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from django.utils.datetime_safe import datetime

from campaigns.models import FileSource
from campaigns.serializers.sources import FileSourceSerializer
from campaigns.serializers.sources.file_source import FileSourceCreateSerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_file_source, basic_campaign
from tests.utils import serialize_date


def fake_file() -> SimpleUploadedFile:
    return SimpleUploadedFile(
        "input.txt",
        b"text content"
    )


def uploaded_file_source() -> FileSource:
    source, _ = FileSource.objects.get_or_create(
        name="file source",
        description="description",
        source_link="http://source.access.link",
        source_date=timezone.now(),
        file=fake_file(),
        campaign=basic_campaign()
    )
    return source


class FileSourceSerializerTestCase(TestCase):
    def test_serialize(self):
        source = basic_file_source(basic_campaign())
        serializer = FileSourceSerializer(source)

        self.assertEqual(
            serializer.data,
            {
                'id': source.id,
                'name': source.name,
                'description': source.description,
                'source_link': source.source_link,
                'source_date': serialize_date(source.source_date),
                'created': serialize_date(source.created),
                'status': source.status,
                'type': source.type,
                'file': None
            }
        )

    def test_serialize_non_empty_file(self):
        source = uploaded_file_source()
        serializer = FileSourceSerializer(source)

        self.assertEqual(
            serializer.data,
            {
                'id': source.id,
                'name': source.name,
                'description': source.description,
                'source_link': source.source_link,
                'source_date': serialize_date(source.source_date),
                'created': serialize_date(source.created),
                'status': source.status,
                'type': source.type,
                'file': source.file.url
            }
        )

    def test_update(self):
        instance = basic_file_source(basic_campaign())

        serializer = FileSourceSerializer(
            instance,
            data={
                'name': "other",
                'description': 'other description'
            },
            partial=True
        )
        serializer.is_valid()
        serializer.save(campaign=instance.campaign)

        self.assertEqual(instance.name, "other")
        self.assertEqual(instance.description, "other description")

    def test_create(self):
        serializer = FileSourceSerializer(
            data={
                'name': "other",
                'description': 'description',
                'source_link': 'http://source.link',
                'source_date': serialize_date(datetime(2021, 12, 24)),
                'file': fake_file()
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()


class FileSourceCreateSerializerTestCase(TestCase):
    def test_serialize(self):
        source = basic_file_source(basic_campaign())
        serializer = FileSourceCreateSerializer(source)

        self.assertEqual(
            serializer.data,
            {
                'id': source.id,
                'name': source.name,
                'description': source.description,
                'source_link': source.source_link,
                'source_date': serialize_date(source.source_date),
                'file': None
            }
        )

    def test_serialize_non_empty_file(self):
        source = uploaded_file_source()
        serializer = FileSourceCreateSerializer(source)

        self.assertEqual(
            serializer.data,
            {
                'id': source.id,
                'name': source.name,
                'description': source.description,
                'source_link': source.source_link,
                'source_date': serialize_date(source.source_date),
                'file': source.file.url
            }
        )

    def test_update(self):
        instance = basic_file_source(basic_campaign())

        serializer = FileSourceCreateSerializer(
            instance,
            data={
                'name': "other",
                'description': 'other description',
                'source_link': 'http://source.link',
                'source_date': serialize_date(datetime(2021, 12, 24)),
                'file': fake_file()
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save(campaign=basic_campaign())

    def test_create(self):
        serializer = FileSourceCreateSerializer(
            data={
                'name': "other",
                'description': 'description',
                'source_link': 'http://source.link',
                'source_date': serialize_date(datetime(2021, 12, 24)),
                'file': fake_file()
            }
        )
        serializer.is_valid()
        serializer.save(campaign=basic_campaign())

        source = FileSource.objects.get(name='other')
        self.assertIsInstance(source, FileSource)
