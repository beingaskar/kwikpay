from django.db import models


class BaseModel(models.Model):
    """ Default Django model extended to provide common fields.
    For auditing, logging etc.
    """

    timestamp_created = models.DateTimeField(
        auto_now_add=True
    )

    timestamp_updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True
