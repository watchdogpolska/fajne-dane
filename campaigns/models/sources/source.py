from django.db import models
from django.utils.translation import gettext_lazy as _


class SourceTypes(models.TextChoices):
    NONE = 'NONE', _('None')
    USER = 'USER', _('User')
    FILE = 'FILE', _('File')


class Source(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=12,
                            choices=SourceTypes.choices,
                            default=SourceTypes.NONE)

    def to_child(self) -> "Source":
        """
        Used to get an object of a child type object.
        """
        import campaigns.models.sources as s
        if self.type == SourceTypes.USER:
            return s.user_source.UserSource.objects.get(id=self.id)
        if self.type == SourceTypes.FILE:
            return s.file_source.FileSource.objects.get(id=self.id)
        raise TypeError(f"No child mapping found for type: {self.type}")
