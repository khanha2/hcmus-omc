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
    contest_time = models.PositiveIntegerField(default=0)
    maximum_of_matches = models.PositiveIntegerField(default=0)

    use_mc_test = models.BooleanField(default=False)
    mc_questions = models.PositiveIntegerField(default=0)

    use_writing_test = models.BooleanField(default=False)

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
            'contest_time',
            'maximum_of_matches',
            'use_mc_test',
            'mc_questions',
            'use_writing_test',
        ]


class ContestUserMixin(BaseModel):
    contest = models.ForeignKey(Contest)
    user = models.ForeignKey(User)

    class Meta:
        abstract = True
        unique_together = ('contest', 'user')

    def delete(self):
        self.is_deleted = True
        super(ContestUserMixin, self).delete()


class ContestManager(ContestUserMixin):
    pass

    # def __unicode__(self):
    #     return '%s - %s' % (str(self.contest.name), str(self.user))


class Contestant(ContestUserMixin):
    participated = models.BooleanField(default=False)

    # def __unicode__(self):
    #     return '%s - %s' % (str(self.contest.name), str(self.user))


class Question(models.Model):
    contest = models.ForeignKey(Contest)
    content = models.TextField(default='')

    class Meta:
        abstract = True

    def __unicode__(self):
        short_cont = self.content if len(
            self.content) <= 30 else self.content[:-30]
        return '%s - %s' % (str(self.contest), short_cont)


class MCQuestion(Question):
    contest = models.ForeignKey(Contest)
    content = models.TextField(default='')
    a = models.TextField(null=True, default=None)
    b = models.TextField(null=True, default=None)
    c = models.TextField(null=True, default=None)
    d = models.TextField(null=True, default=None)
    answer = models.CharField(max_length=2, null=True, default=None)

    @staticmethod
    def get_field_list():
        return ['content', 'a', 'b', 'c', 'd', 'answer']


class WritingQuestion(Question):

    @staticmethod
    def get_field_list():
        return ['content']


class Match(BaseModel):
    contestant = models.ForeignKey(Contestant)
    match_id = models.PositiveSmallIntegerField()

    writing_questions = models.TextField(
        null=True, blank=True, default='[]')
    writing_responses = models.TextField(
        null=True, blank=True, default='{}')

    mc_questions = models.TextField(null=True, blank=True, default='[]')
    mc_responses = models.TextField(null=True, blank=True, default='{}')
    mc_passed_responses = models.PositiveIntegerField(default=0)

    start_time = models.DateTimeField(null=True, blank=True, default=None)
    end_time = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('contestant', 'match_id')

    def save(self, *args, **kwargs):
        super(Match, self).save(*args, **kwargs)

    # def __unicode__(self):
    #     return '%s' % str(self.contestant)


# auditlog.register(Contest)
# auditlog.register(ContestManager)
# auditlog.register(Contestant)
# auditlog.register(Match)
