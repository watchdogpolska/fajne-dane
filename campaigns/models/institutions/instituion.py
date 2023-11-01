from django.db import models

from campaigns.exceptions import InstitutionParentGroupMissmatch, InstitutionGroupHasNoParent


class Institution(models.Model):
    """
    """
    group = models.ForeignKey("InstitutionGroup",
                             on_delete=models.CASCADE,
                             related_name="institutions")

    parent = models.ForeignKey("Institution",
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name="children")

    key = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    link = models.CharField(max_length=64, default=None, null=True, blank=True)
    address = models.CharField(max_length=64, default=None, null=True, blank=True)
    metadata = models.JSONField(default=dict)

    def set_parent(self, parent: "Institution"):
        if not self.parent.parent:
            raise InstitutionGroupHasNoParent()
        if parent.group != self.parent.parent:
            raise InstitutionParentGroupMissmatch()
        self.parent = parent
