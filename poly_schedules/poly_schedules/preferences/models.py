"""
.. module:: poly_schedules.preferences.models
   :synopsis: Poly Schedules Preference Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.conf import settings
from django.db.models import Model
from django.db.models.fields import PositiveSmallIntegerField, BooleanField
from django.db.models.fields.related import ForeignKey

from ..schedules.models import Course, Term, Week


class CoursePreference(Model):
    """An instructor's course preference."""

    PREFERENCE_CHOICES = [(x, x) for x in xrange(6)]

    term = ForeignKey(Term)
    instructor = ForeignKey(settings.AUTH_USER_MODEL)
    course = ForeignKey(Course)
    preference = PositiveSmallIntegerField(default=0, verbose_name='', choices=PREFERENCE_CHOICES)

    def __unicode__(self):
        return "Course Preference (%s)" % unicode(self.id)


class TimePreference(Model):
    """An instructor's time preference."""

    term = ForeignKey(Term)
    instructor = ForeignKey(settings.AUTH_USER_MODEL)
    availability = ForeignKey(Week, null=True, blank=True)

    def __unicode__(self):
        return "Time Preference (%s)" % unicode(self.id)


class TermPreferenceLock(Model):
    """Boolean container for whether or not an instructor's preferences have been manually locked."""

    term = ForeignKey(Term)
    instructor = ForeignKey(settings.AUTH_USER_MODEL)
    locked = BooleanField(default=False)

    def __unicode__(self):
        return "Term Preference Lock (%s)" % unicode(self.id)
