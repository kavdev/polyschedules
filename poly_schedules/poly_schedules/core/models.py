"""
.. module:: poly_schedules.core.models
   :synopsis: Poly Schedules Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import re

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BooleanField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from preferences.models import CoursePreference
from schedules.models import Week


class PolySchedulesUser(AbstractUser):
    """Poly Schedules User Model."""

    # Special Instructor Fields
    max_wtu = PositiveIntegerField(default=8)
    course_preferences = ManyToManyField(CoursePreference, blank=True)
    time_preference = ForeignKey(Week, null=True, blank=True)
    preferences_locked = BooleanField(default=False)
    is_active_instructor = BooleanField(default=True)

    #
    # A set of flags for each user that decides what s/he can and cannot see.
    #
    is_instructor = BooleanField(default=False)

    class Meta:
        verbose_name = u'Poly Schedules User'
        verbose_name_plural = u'Poly Schedules Users'

    def get_full_name(self):
        """Returns the first_name plus the last_name with a space in between and the possible '- ADMIN' removed."""

        full_name = '%s %s' % (self.first_name, re.sub(r' - ADMIN', '', self.last_name))
        return full_name.strip()

    def get_alias(self):
        """Returns the username with the possible '-admin' removed."""

        return re.sub(r'-admin', '', self.username)
