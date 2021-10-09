from campaigns.models import Campaign, Document, Query, OutputField, FileSource, UserSource
from campaigns.models.factory import campaign_factory
from tests.unit.campaigns.conftest import basic_campaign_template, user1


def basic_user_source() -> UserSource:
    source, _ = UserSource.objects.get_or_create(
        name="user's source",
        user=user1()
    )
    return source


def basic_file_source() -> FileSource:
    source, _ = FileSource.objects.get_or_create(
        name="file source"
    )
    return source


def basic_campaign():
    campaign, _ = Campaign.objects.get_or_create(
        name="test1",
        template=basic_campaign_template()
    )
    return campaign

def basic_campaign_with_queries():
    return campaign_factory.create("basic", basic_campaign_template())


def basic_document():
    campaign = basic_campaign()
    return Document.objects.create(
        campaign=campaign,
        source=basic_file_source(),
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
