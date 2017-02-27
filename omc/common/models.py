from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

from auditlog.models import AuditlogHistoryField
# Create your models here.


class BaseModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    deleted_date = models.DateTimeField(null=True, blank=True, default=None)

    history = AuditlogHistoryField()

    class Meta:
        abstract = True

    def delete(self):
        if self.is_deleted:
            super(BaseModel, self).delete()
        else:
            self.is_deleted = True
            self.deleted_date = timezone.now()
            self.save()
