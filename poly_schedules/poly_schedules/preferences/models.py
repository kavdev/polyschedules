"""
.. module:: poly_schedules.preferences.models
   :synopsis: Poly Schedules Preference Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.db.models import Model
from django.db.models.fields import PositiveSmallIntegerField, BooleanField
from django.db.models.fields.related import ForeignKey

from ..schedules.models import Course, Term, Week


class CoursePreference(Model):
    """An instructor's course preference."""

    PREFERENCE_CHOICES = [(x, x) for x in xrange(6)]

    term = ForeignKey(Term)
    course = ForeignKey(Course)
    preference = PositiveSmallIntegerField(default=0, verbose_name='', choices=PREFERENCE_CHOICES)
    locked = BooleanField(default=False)


class TimePreference(Model):
    """An instructor's time preference."""

    term = ForeignKey(Term)
    availability = ForeignKey(Week, null=True, blank=True)
    locked = BooleanField(default=False)
