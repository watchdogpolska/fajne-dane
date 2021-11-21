from campaigns.models import Document
from tests.campaigns.conftest import basic_campaign, basic_file_source


def basic_document():
    return Document.objects.create(
        campaign=basic_campaign(),
        data={"institution_id": "234"},
        source=basic_file_source()
    )

