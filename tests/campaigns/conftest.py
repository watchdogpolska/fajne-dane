from typing import List, Dict

from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone

from campaigns.models import Campaign, DocumentQuery, Institution, InstitutionGroup
from campaigns.models import Document, Query, OutputField, FileSource, UserSource
from campaigns.models.dto import DocumentDTO
from campaigns.models.factory import campaign_factory, InstitutionsFactory
from campaigns.models.factory.documents_factory import DocumentsFactory
from campaigns.parsers import institutions_file_parser
from campaigns.parsers.campaign_dataset_parser import CampaignDatasetParser
from tests.conftest import (
    basic_campaign_template, advanced_campaign_template,
    basic_campaign_dataset, advanced_campaign_dataset,
    user1, basic_institutions_file, basic_campaign_documents_file, wrong_advanced_campaign_documents_file
)


def invalid_campaign_template() -> Dict:
    return {'type': 'object', 'properties': {'value': {'type': 'any'}}}


def basic_campaign() -> Campaign:
    campaign, _ = Campaign.objects.get_or_create(
        name="test1",
        institution_group=basic_institution_group(),
        template=basic_campaign_template()
    )
    return campaign


def basic_campaign_with_queries() -> Campaign:
    campaign = Campaign.objects.filter(name="basic").first()
    if not campaign:
        campaign = campaign_factory.create(
            "basic",
            basic_institution_group(),
            basic_campaign_template()
        )
    return campaign


def advanced_campaign_with_queries() -> Campaign:
    campaign = Campaign.objects.filter(name="advanced").first()
    if not campaign:
        campaign = campaign_factory.create(
            "advanced",
            basic_institution_group(),
            advanced_campaign_template()
        )
    return campaign


def basic_campaign_with_documents() -> Campaign:
    setup_institutions()
    factory = basic_campaign_documents_factory()
    document_dtos = basic_campaign_dtos()
    factory.bulk_create(document_dtos)
    return factory.campaign


def advanced_campaign_with_documents() -> Campaign:
    setup_institutions()
    factory = advanced_campaign_documents_factory()
    document_dtos = advanced_campaign_dtos()
    factory.bulk_create(document_dtos)
    return factory.campaign


def basic_user_source() -> UserSource:
    source, _ = UserSource.objects.get_or_create(
        name="user's source",
        user=user1()
    )
    return source


def basic_file_source(campaign: Campaign) -> FileSource:
    source, _ = FileSource.objects.get_or_create(
        campaign=campaign,
        name="file source",
        description="description",
        source_link="http://source.access.link",
        source_date=timezone.now(),
        file=None
    )
    return source


def basic_document():
    campaign = advanced_campaign_with_queries()
    return Document.objects.create(
        campaign=campaign,
        source=basic_file_source(campaign),
        data={},
        institution=basic_institution()
    )


def basic_query() -> Query:
    campaign = basic_campaign()
    return Query.objects.create(
        campaign=campaign,
        order=0,
        name="question 1",
        data={
            "question": {
                "name": "question",
                "value": "What is it?",
                "type": "str",
                "widget": "label"
            }
        },
        output_field=OutputField.objects.create(
            name="test_field",
            widget="text_label",
            type="str",
            validation=False,
            default_answer=0
        )
    )


def basic_document_query() -> DocumentQuery:
    return DocumentQuery.objects.create(
        document=basic_document(),
        query=basic_query()
    )


def basic_campaign_documents_factory() -> DocumentsFactory:
    campaign = basic_campaign_with_queries()
    return DocumentsFactory(
        campaign=campaign,
        source=basic_file_source(campaign)
    )


def advanced_campaign_documents_factory() -> DocumentsFactory:
    campaign = advanced_campaign_with_queries()
    return DocumentsFactory(
        campaign=campaign,
        source=basic_file_source(campaign)
    )


def basic_campaign_data_frame_parser() -> CampaignDatasetParser:
    return CampaignDatasetParser(
        campaign=basic_campaign_with_queries()
    )


def advanced_campaign_data_frame_parser() -> CampaignDatasetParser:
    return CampaignDatasetParser(
        campaign=advanced_campaign_with_queries()
    )


def advanced_campaign_dtos() -> List[DocumentDTO]:
    """
    Documents are created from the advanced_campaign dataset using a DataFrameParser.

    :return: A list of DocumentDTOs parsed from the test dataset.
    """
    parser = advanced_campaign_data_frame_parser()
    _, documents = parser.parse(advanced_campaign_dataset())
    return documents


def basic_campaign_dtos() -> List[DocumentDTO]:
    """
    Documents are created from the basic campaign dataset using a DataFrameParser.

    :return: A list of DocumentDTOs parsed from the test dataset.
    """
    parser = basic_campaign_data_frame_parser()
    _, documents = parser.parse(basic_campaign_dataset())
    return documents


def basic_institution_group() -> InstitutionGroup:
    group, _ = InstitutionGroup.objects.get_or_create(
        name="test_group",
    )
    return group


def child_institution_group() -> InstitutionGroup:
    group, _ = InstitutionGroup.objects.get_or_create(
        name="test_group",
        parent=basic_institution_group()
    )
    return group


def basic_institution() -> Institution:
    institution, _ = Institution.objects.get_or_create(
        key="1",
        name="test_1",
        group=basic_institution_group()
    )
    return institution


def child_institution() -> Institution:
    institution, _ = Institution.objects.get_or_create(
        key="2",
        parent=basic_institution(),
        name="test_2",
        group=basic_institution_group()
    )
    return institution


def setup_institutions() -> List[Institution]:
    if Institution.objects.count():
        return Institution.objects.all()
    institutions_file = basic_institutions_file()
    institutions_dtos = institutions_file_parser.parse(institutions_file)
    group = basic_institution_group()
    return InstitutionsFactory(group).bulk_create(institutions_dtos)


def fake_file() -> SimpleUploadedFile:
    with basic_campaign_documents_file(mode='rb') as f:
        return SimpleUploadedFile(
            "input.txt",
            f.read()
        )


def file_source_with_file() -> FileSource:
    return FileSource.objects.create(
        name="file source",
        description="this is a file",
        campaign=basic_campaign_with_queries(),
        source_link="http://source.link",
        source_date=timezone.now(),
        file=fake_file(),
    )


def file_source_with_wrong_data_file() -> FileSource:
    return FileSource.objects.create(
        name="file source",
        description="this is a file",
        campaign=basic_campaign_with_queries(),
        source_link="http://source.link",
        source_date=timezone.now(),
        file=wrong_data_fake_file(),
    )


def wrong_data_fake_file() -> SimpleUploadedFile:
    with wrong_advanced_campaign_documents_file(mode='rb') as f:
        return SimpleUploadedFile(
            "wrong_input.txt",
            f.read()
        )
