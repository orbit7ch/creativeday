from django.contrib.postgres.fields import JSONField
from django_extensions.db.models import TimeStampedModel
from django.db import models


class GenericEvent(TimeStampedModel):
    title = models.TextField()
    fields = JSONField()

    session_id = models.CharField(max_length=512, null=True, blank=True)
    ga_id = models.CharField(max_length=512, null=True, blank=True)
    is_internal = models.BooleanField(default=False)

    reported = models.BooleanField(default=False)

    @property
    def fields_clean(self):
        try:
            return ', '.join(['%s: %s' % (k, v) for k, v in list(self.fields.items())])
        except:
            pass
        return ''
