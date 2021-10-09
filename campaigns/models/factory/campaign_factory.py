from typing import Dict

from campaigns.models import Campaign
from campaigns.serializers import QuerySerializer
from campaigns.serializers.document_data_field import DocumentDataFieldSerializer
from campaigns.validators.template import validate_campaign_template


def _create_campaign(name: str, template: Dict) -> Campaign:
    return Campaign.objects.create(
        name=name,
        template=template
    )


def _create_document_fields(campaign: Campaign, document_template: Dict):
    for field_template in document_template['data_fields']:
        serializer = DocumentDataFieldSerializer(data=field_template)
        serializer.is_valid()
        serializer.save(campaign=campaign)


def _create_queries(campaign, query_templates: Dict):
    for raw_query in query_templates:
        raw_query['data'] = raw_query.pop('data_fields')
        serializer = QuerySerializer(data=raw_query)
        serializer.is_valid()
        serializer.save(campaign=campaign)


def create(name: str, template: Dict) -> Campaign:
    """
    Used provided name and template to create a new campaign.
    Provided template is then parsed and used to create DocumentDataFields and Queries.

    :param name: name of the campaign
    :param template: template of the campaign
    :return: newly created campaign
    """
    validate_campaign_template(template)
    campaign = _create_campaign(name, template)

    _create_document_fields(campaign, template['document'])
    _create_queries(campaign, template['queries'])

    return campaign
