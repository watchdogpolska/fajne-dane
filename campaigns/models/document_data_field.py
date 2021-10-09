from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from campaigns.models.dto import DocumentDTO
from campaigns.validators.type import validate_type


class DocumentDataField(models.Model):
    """
    """

    campaign = models.ForeignKey("Campaign",
                                 on_delete=models.CASCADE,
                                 related_name="document_fields")
    name = models.CharField(max_length=64)
    widget = models.CharField(max_length=64)
    type = models.CharField(max_length=10)

    def validate(self, document: DocumentDTO):
        errors = []
        try:
            value = document.data[self.name]
            validate_type(value, self.type)
        except KeyError:
            errors.append(
                ValidationError(
                    _("Field: %(value)s not found in the document data."),
                    code='missing-field',
                    params={'value': self.name}
                )
            )
        except ValidationError as e:
            errors.append(e)

        if errors:
            raise ValidationError(errors)
