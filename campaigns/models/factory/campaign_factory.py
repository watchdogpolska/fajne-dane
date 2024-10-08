from typing import Dict

from campaigns.models import Campaign, InstitutionGroup
from campaigns.serializers import QueryCreateSerializer
from campaigns.serializers.document_data_field import DocumentDataFieldCreateSerializer
from campaigns.validators.template import validate_campaign_template
from reports.models import DataSource


def _create_campaign(name: str, institution_group: InstitutionGroup, template: Dict) -> Campaign:
    return Campaign.objects.create(
        name=name,
        institution_group=institution_group,
        template=template
    )


def _create_document_fields(campaign: Campaign, document_template: Dict):
    for field_template in document_template.get('data_fields', []):
        serializer = DocumentDataFieldCreateSerializer(data=field_template)
        serializer.is_valid()
        serializer.save(campaign=campaign)


def _create_queries(campaign, query_templates: Dict):
    for raw_query in query_templates:
        raw_query['data'] = raw_query.pop('data_fields')
        serializer = QueryCreateSerializer(data=raw_query)
        serializer.is_valid()
        serializer.save(campaign=campaign)


def create(name: str, institution_group: InstitutionGroup, template: Dict) -> Campaign:
    """
    Used provided name and template to create a new campaign.
    Provided template is then parsed and used to create DocumentDataFields and Queries.

    :param name: name of the campaign
    :param institution_group: leaf institution group
    :param template: template of the campaign
    :return: newly created campaign
    """
    validate_campaign_template(template)
    campaign = _create_campaign(name, institution_group, template)
    DataSource.objects.create(campaign=campaign)

    _create_document_fields(campaign, template['document'])
    _create_queries(campaign, template['queries'])

    return campaign
