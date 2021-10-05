from django.test import TestCase

from campaigns.models import Campaign, Query
from tests.unit.campaigns.conftest import basic_campaign_template


class QueryTestCase(TestCase):
    def setUp(self):
        Campaign.objects.create(
            name="test1",
            template=basic_campaign_template()
        )

    def test_creating(self):
        Query.objects.create(
            campaign=Campaign.objects.first(),
            order=0,
            name="question 1",
            data={
                "question": {
                    "name": "question",
                    "value": "What is it?",
                    "type": "str",
                    "widget": "label"
                }
            }
        )


        campaign = models.ForeignKey("Campaign",
                                     on_delete=models.CASCADE,
                                     related_name="queries")
    order = models.IntegerField()
    name = models.CharField(max_length=20)
    data = models.JSONField(default=dict)

    output_field = models.OneToOneField(OutputField,
                                        on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('order', )
