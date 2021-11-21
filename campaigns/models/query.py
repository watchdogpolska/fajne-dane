from django.db import models

from campaigns.models.dto import RecordDTO
from campaigns.models.output_field import OutputField


class Query(models.Model):
    """
    Query specifies a question that is asked to the document.
    One campaign can have multiple Queries.
    Query objects should be created based on the template of the Campaign.
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

    def validate_record(self, record: RecordDTO):
        """
        Validated records value using Query's OutputField.

        :raises: ValidationError
        """
        self.output_field.validate(record)
