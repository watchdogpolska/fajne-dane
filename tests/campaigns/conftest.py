from typing import List, Dict

from campaigns.models import Campaign
from campaigns.models import Document, Query, OutputField, FileSource, UserSource
from campaigns.models.dto import DocumentDTO
from campaigns.models.factory import campaign_factory
from campaigns.models.factory.documents_factory import DocumentsFactory
from campaigns.parsers.data_frame_parser import DataFrameParser
from tests.conftest import (
    basic_campaign_template, advanced_campaign_template,
    basic_campaign_dataset, advanced_campaign_dataset,
    user1
)


def invalid_campaign_template() -> Dict:
    return {'type': 'object', 'properties': {'value': {'type': 'any'}}}


def basic_campaign() -> Campaign:
    campaign, _ = Campaign.objects.get_or_create(
        name="test1",
        template=basic_campaign_template()
    )
    return campaign


def basic_campaign_with_queries() -> Campaign:
    campaign = Campaign.objects.filter(name="basic").first()
    if not campaign:
        campaign = campaign_factory.create("basic", basic_campaign_template())
    return campaign


def advanced_campaign_with_queries() -> Campaign:
    campaign = Campaign.objects.filter(name="advanced").first()
    if not campaign:
        campaign = campaign_factory.create("advanced", advanced_campaign_template())
    return campaign


def basic_campaign_with_documents() -> Campaign:
    factory = basic_campaign_documents_factory()
    document_dtos = basic_campaign_dtos()
    factory.bulk_create(document_dtos)
    return factory.campaign


def advanced_campaign_with_documents() -> Campaign:
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
        file=None
    )
    return source


def basic_document():
    campaign = basic_campaign()
    return Document.objects.create(
        campaign=campaign,
        source=basic_file_source(campaign),
        data={"institution_id": 1}
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


def basic_campaign_data_frame_parser() -> DataFrameParser:
    return DataFrameParser(
        campaign=basic_campaign_with_queries()
    )


def advanced_campaign_data_frame_parser() -> DataFrameParser:
    return DataFrameParser(
        campaign=advanced_campaign_with_queries()
    )


def advanced_campaign_dtos() -> List[DocumentDTO]:
    """
    Documents are created from the advanced_campaign dataset using a DataFrameParser.

    :return: A list of DocumentDTOs parsed from the test dataset.
    """
    parser = advanced_campaign_data_frame_parser()
    parsing_report = parser.parse(advanced_campaign_dataset())
    return parsing_report.documents


def basic_campaign_dtos() -> List[DocumentDTO]:
    """
    Documents are created from the basic campaign dataset using a DataFrameParser.

    :return: A list of DocumentDTOs parsed from the test dataset.
    """
    parser = basic_campaign_data_frame_parser()
    parsing_report = parser.parse(basic_campaign_dataset())
    return parsing_report.documents

