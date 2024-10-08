from django.db import models

from users.models.user import User
from .source import Source, SourceTypes


class UserSource(Source):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="source")

    def __init__(self, *args, **kwargs):
        if 'type' not in kwargs:
            kwargs['type'] = SourceTypes.USER
        super().__init__(*args, **kwargs)
