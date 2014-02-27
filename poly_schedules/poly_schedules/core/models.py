"""
.. module:: poly_schedules.core.models
   :synopsis: Poly Schedules Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import re

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BooleanField, PositiveIntegerField
from django.db.models.fields.related import ManyToManyField

from ..preferences.models import CoursePreference, TimePreference
from ..schedules.models import Course, Term, Week


class PolySchedulesUser(AbstractUser):
    """Poly Schedules User Model."""

    # Special Instructor Fields
    max_wtu = PositiveIntegerField(default=8)
    course_preferences = ManyToManyField(CoursePreference, blank=True)
    time_preference = ManyToManyField(TimePreference, blank=True)
    is_active_instructor = BooleanField(default=True)

    #
    # A set of flags for each user that decides what s/he can and cannot see.
    #
    is_instructor = BooleanField(default=False)

    def get_full_name(self):
        """Returns the first_name plus the last_name with a space in between and the possible '- ADMIN' removed."""

        full_name = '%s %s' % (self.first_name, re.sub(r' - ADMIN', '', self.last_name))
        return full_name.strip()

    def get_alias(self):
        """Returns the username with the possible '-admin' removed."""

        return re.sub(r'-admin', '', self.username)

    def initialize_preferences(self):
        """Initialises course and time preferences for instructors."""

        if self.is_instructor:
            # Initialize course preferences
            for course in Course.objects.all():
                course_pref, created = CoursePreference.objects.get_or_create(term=Term().get_or_create_current_term(), course=course)

                if created:
                    self.course_preferences.add(course_pref)
                    self.save()

            # Initialize time preference
            time_pref, created = TimePreference.objects.get_or_create(term=Term().get_or_create_current_term())

            if created:
                week = Week()
                week.save()
                time_pref.availability = week
                time_pref.save()
                self.time_preference.add(time_pref)
                self.save()

    class Meta:
        verbose_name = u'PolySchedules User'
        verbose_name_plural = u'PolySchedules Users'
