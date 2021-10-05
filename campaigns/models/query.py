from django.db import models

from campaigns.models.output_field import OutputField
from campaigns.validators.query import validate_query_integrity


class Query(models.Model):
    """
    Query specifies a question that is asked to the document.
    One campaign can have multiple Queries.
    Query objects should be created based on the template of the Campaign.
    If any changes in the structure will cause ValidationError.
    """

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

    def clean(self):
        cleaned_data = super().clean()
        if hasattr(self, 'campaign'):
            template = self.campaign.campaign_template
            query_template = template.query_schemas.get(self.name)
            validate_query_integrity(query_template, self)
        return cleaned_data

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
