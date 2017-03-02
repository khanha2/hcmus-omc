from __future__ import unicode_literals

from django.db import models

from auditlog.registry import auditlog

from common.models import BaseModel
from users.models import User
# Create your models here.


class Contest(BaseModel):
    name = models.CharField(max_length=200)
    from_time = models.DateTimeField(null=True, blank=True, default=None)
    to_time = models.DateTimeField(null=True, blank=True, default=None)
    short_description = models.TextField(null=True, blank=True, default=None)
    description = models.TextField(null=True, blank=True, default=None)

    use_mc_test = models.BooleanField(default=False)
    mc_test_time = models.PositiveIntegerField(default=0)
    mc_test_questions = models.PositiveIntegerField(default=0)

    use_writing_test = models.BooleanField(default=False)
    writing_test_time = models.PositiveIntegerField(default=0)
    
    def __unicode__(self):
        return '%s' % (self.name)

    @staticmethod
    def get_field_list():
        return [
            'name',
            'from_time',
            'to_time',
            'short_description',
            'description',
            'use_mc_test',
            'mc_test_time',
            'mc_test_questions',
            'use_writing_test'
        ]


class ContestManager(BaseModel):
    contest = models.ForeignKey(Contest)
    user = models.ForeignKey(User)

    class Meta:
        unique_together = ('contest', 'user')

    def __unicode__(self):
        return '%s - %s' % (str(self.contest), str(self.user))

# class Contestant(BaseModel):
#     pass

auditlog.register(Contest)
auditlog.register(ContestManager)
