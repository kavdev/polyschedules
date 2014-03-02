"""
.. module:: poly_schedules.core.models
   :synopsis: Poly Schedules Core Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import re

from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BooleanField, PositiveIntegerField
from django.db.models.fields.related import ForeignKey, ManyToManyField

from ..preferences.models import CoursePreference, TimePreference, TermPreferenceLock
from ..schedules.models import Course, Week, Term


class PolySchedulesUser(AbstractUser):
    """Poly Schedules User Model."""

    # Special Instructor Fields
    max_wtu = PositiveIntegerField(default=8)
    course_preferences = ManyToManyField(CoursePreference, blank=True)
    time_preference = ManyToManyField(TimePreference, blank=True)
    preference_locks = ManyToManyField(TermPreferenceLock, blank=True)
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

    def initialize_preferences(self, term_id):
        """Initialises course and time preferences for instructors."""

        if self.is_instructor:
            term = Term.objects.get(id=term_id)

            # Initialize term lock
            term_preference_lock, created = self.preference_locks.select_related().get_or_create(term=term, instructor=self)

            if created:
                term_preference_lock.save()
                self.preference_locks.add(term_preference_lock)
                self.save()

            # Initialize course preferences
            for course in Course.objects.all():
                course_pref, created = self.course_preferences.select_related().get_or_create(term=term, instructor=self, course=course)

                if created:
                    self.course_preferences.add(course_pref)
                    self.save()

            # Initialize time preference
            time_pref, created = self.time_preference.select_related().get_or_create(term=term, instructor=self)

            if created:
                week = Week()
                week.save()
                time_pref.availability = week
                time_pref.save()
                self.time_preference.add(time_pref)
                self.save()

    def __unicode__(self):
        return unicode(self.get_full_name())

    class Meta:
        verbose_name = u'PolySchedules User'
        verbose_name_plural = u'PolySchedules Users'
