from __future__ import unicode_literals

from django.db import models

from common.models import BaseModel
from users.models import User
# Create your models here.


class Contest(BaseModel):
    name = models.CharField(max_length=200)
    from_time = models.DateTimeField(null=True, blank=True, default=None)
    to_time = models.DateTimeField(null=True, blank=True, default=None)
    short_description = models.TextField(null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)

    def __unicode__(self):
        return '%s' % (self.name)


class ContestManager(BaseModel):
    contest = models.ForeignKey(Contest)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('contest', 'user')

    def __unicode__(self):
        return '%s - %s' % (str(self.contest), str(self.user))
