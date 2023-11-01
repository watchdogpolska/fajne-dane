from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.db.models import Manager
from django.test import TestCase

from campaigns.models import Document
from campaigns.models.campaign import Campaign, CampaignStatus
from campaigns.models.dto import DocumentDTO, RecordDTO, InstitutionDTO
from tests.conftest import basic_campaign_template
from tests.campaigns.conftest import basic_campaign_with_queries, \
    advanced_campaign_with_queries, basic_campaign_with_documents, basic_institution_group, setup_institutions, \
    child_institution_group


class CampaignTestCase(TestCase):

    def test_validating_wrong_document(self):
        campaign = basic_campaign_with_queries()
        with self.assertRaises(ValidationError):
            campaign.validate_document(
                DocumentDTO(
                    institution=InstitutionDTO(),
                    data={"project_id": 1}
                )
            )

    def test_creating(self):
        campaign, _ = Campaign.objects.get_or_create(
            name="test1",
            institution_group=basic_institution_group(),
            template=basic_campaign_template()
        )
        self.assertIsInstance(campaign, Campaign)
        self.assertEqual(campaign.status, CampaignStatus.CREATED)
        self.assertIsInstance(campaign.template, dict)

    def test_data_field_objects_cache(self):
        # sourcery skip: extract-duplicate-method
        campaign = advanced_campaign_with_queries()
        fields = list(campaign.document_fields.all())

        with patch.object(Manager, 'all', return_value=fields) as mock_method:
            fields_objects = campaign.document_fields_objects
            self.assertEqual(fields_objects, fields)
            self.assertEqual(mock_method.call_count, 1)

            fields_objects = campaign.document_fields_objects
            self.assertEqual(fields_objects, fields)
            self.assertEqual(mock_method.call_count, 1)

    def test_data_queries_cache(self):
        # sourcery skip: extract-duplicate-method
        campaign = advanced_campaign_with_queries()
        fields = list(campaign.queries.all())

        with patch.object(Manager, 'all', return_value=fields) as mock_method:
            queries_objects = campaign.queries_objects
            self.assertEqual(queries_objects, fields)
            self.assertEqual(mock_method.call_count, 1)

            queries_objects = campaign.queries_objects
            self.assertEqual(queries_objects, fields)
            self.assertEqual(mock_method.call_count, 1)

    def test_validating_correct_document(self):
        campaign = basic_campaign_with_queries()
        try:
            campaign.validate_document(
                DocumentDTO(
                    institution=InstitutionDTO(id=1),
                    data={},
                )
            )
        except ValidationError:
            self.fail()

    def test_validating_correct_document_with_record(self):
        campaign = basic_campaign_with_queries()
        try:
            campaign.validate_document(
                DocumentDTO(
                    institution=InstitutionDTO(id=1),
                    data={},
                    records={
                        "question": [
                            RecordDTO(
                                value="yes",
                                probability=0.4
                            )
                        ]
                    }
                )
            )
        except ValidationError:
            self.fail()

    def test_institution_groups_path(self):
        campaign = basic_campaign_with_queries()
        self.assertEqual(campaign.institution_groups_path, [campaign.institution_group.id])


    def test_institution_groups_path_nested(self):
        setup_institutions()
        campaign, _ = Campaign.objects.get_or_create(
            name="test2",
            institution_group=child_institution_group(),
            template=basic_campaign_template()
        )
        self.assertEqual(campaign.institution_groups_path,
                         [campaign.institution_group.id, campaign.institution_group.parent.id])


    def test_validating_correct_document_wrong_record(self):
        campaign = basic_campaign_with_queries()
        with self.assertRaises(ValidationError):
            campaign.validate_document(
                DocumentDTO(
                    institution=InstitutionDTO(id=1),
                    data={},
                    records={
                        "Question 0": [
                            RecordDTO(
                                value="maybe",
                                probability=0.4
                            )
                        ]
                    }
                )
            )


class CampaignStatusTestCase(TestCase):
    def _close_document(self, document: Document):
        for dq in document.document_queries.all():
            record = dq.records.first()
            dq.accept_records([record])

    def setUp(self):
        self.campaign = basic_campaign_with_documents()
        self.document = self.campaign.documents.get(institution__key="1425011")

    def test_close_one_document(self):
        document = self.campaign.documents.first()
        campaign = self.campaign

        self.assertEqual(campaign.status, CampaignStatus.VALIDATING)
        self._close_document(document)
        campaign.refresh_from_db()
        self.assertEqual(campaign.status, CampaignStatus.VALIDATING)


    def test_close_all_documents(self):
        campaign = self.campaign

        self.assertEqual(campaign.status, CampaignStatus.VALIDATING)
        # sourcery skip: no-loop-in-tests
        for document in campaign.documents.all():
            self._close_document(document)
        campaign.refresh_from_db()
        self.assertEqual(campaign.status, CampaignStatus.CLOSED)
