from django.test import TestCase

from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer, CampaignCreateSerializer, CampaignFullSerializer
from fajne_dane.core.exceptions import NotSupported
from tests.campaigns.conftest import basic_campaign
from tests.conftest import basic_campaign_template
from tests.utils import serialize_date


class CampaignSerializerTestCase(TestCase):

    def test_serialize(self):
        campaign = basic_campaign()
        serializer = CampaignSerializer(campaign)
        self.assertEqual(
            serializer.data,
            {
                'id': campaign.id,
                'name': campaign.name,
                'status': campaign.status,
                'created': serialize_date(campaign.created)
            }
        )

    def test_update(self):
        instance = basic_campaign()

        serializer = CampaignSerializer(
            instance,
            data={
                "name": "new"
            }
        )
        serializer.is_valid()
        serializer.save()

        instance.refresh_from_db()
        self.assertEqual(instance.name, "new")

    def test_create(self):
        serializer = CampaignSerializer(
            data={
                "name": "new"
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()


class CampaignFullSerializerTestCase(TestCase):

    def test_serialize(self):
        campaign = basic_campaign()
        serializer = CampaignFullSerializer(campaign)
        self.assertEqual(
            serializer.data,
            {
                'id': campaign.id,
                'name': campaign.name,
                'status': campaign.status,
                'created': serialize_date(campaign.created),
                'template': campaign.template
            }
        )

    def test_update(self):
        instance = basic_campaign()

        serializer = CampaignFullSerializer(
            instance,
            data={
                "name": "new"
            }
        )
        serializer.is_valid()
        serializer.save()

        instance.refresh_from_db()
        self.assertEqual(instance.name, "new")

    def test_create(self):
        serializer = CampaignFullSerializer(
            data={
                "name": "new"
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()


class CampaignCreateSerializerTestCase(TestCase):

    def test_serialize(self):
        campaign = basic_campaign()
        serializer = CampaignCreateSerializer(campaign)
        self.assertEqual(
            serializer.data,
            {
                'id': campaign.id,
                'name': campaign.name,
                'template': campaign.template,
                'status': campaign.status
            }
        )

    def test_update(self):
        instance = basic_campaign()

        serializer = CampaignCreateSerializer(
            instance,
            data={
                "name": "new",
                "template": basic_campaign_template()
            }
        )
        serializer.is_valid()
        with self.assertRaises(NotSupported):
            serializer.save()

    def test_create(self):
        serializer = CampaignCreateSerializer(
            data={
                "name": "new",
                "template": basic_campaign_template()
            }
        )
        serializer.is_valid()
        serializer.save()

        campaign = Campaign.objects.get(name="new")
        self.assertIsInstance(campaign, Campaign)
        self.assertEqual(len(campaign.document_fields_objects), 1)
        self.assertEqual(len(campaign.queries_objects), 1)
