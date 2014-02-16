"""
.. module:: poly_schedules.schedules.models
   :synopsis: Poly Schedules Schedule Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import datetime

from django.conf import settings
from django.db.models import Model, ForeignKey, ManyToManyField, CharField, IntegerField, BooleanField

from .fields import BooleanListField


class Course(Model):
    PROXIMITIES = ['After', 'Same', 'Different']

    prefix = CharField(max_length=4)
    number = IntegerField()
    title = CharField(max_length=60)
    units = IntegerField()
    has_lab = BooleanField()
    lab_length = IntegerField()
    lab_time_proximity = IntegerField()


class Location(Model):
    building = CharField(max_length=60)
    building_number = CharField(max_length=4)
    room_number = CharField(max_length=4)
    has_equipment = IntegerField()
    capacity = IntegerField()
    availability = ManyToManyField('Day')


class Section(Model):
    course = ForeignKey(Course)
    number = IntegerField()
    instructor = ForeignKey(settings.AUTH_USER_MODEL)
    location = ForeignKey(Location)
    times = ManyToManyField('Day')


class Schedule(Model):
    sections = ManyToManyField(Section)


class Day(Model):

    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    day_index = IntegerField()
    availability = BooleanListField()


class Term(Model):

    SEASONS = ['Fall', 'Winter', 'Spring', 'Summer']
    SEASON_CHOICES = [(SEASONS.index(season), season) for season in SEASONS]

    season_index = IntegerField(choices=SEASON_CHOICES)
    year = IntegerField()
    schedule = ForeignKey(Schedule, null=True, blank=True)
    available_sections = ManyToManyField(Section, blank=True)
    preferences_locked = BooleanField(default=False)
    votes_locked = BooleanField(default=False)

    def __unicode__(self):
        return self.SEASONS[self.season_index] + " " + str(self.year)

    def get_current_term(self):
        today = datetime.date.today()

        # Convert date to month and day as integer (md), e.g. 4/21 = 421, 11/17 = 1117, etc.
        # See: http://stackoverflow.com/questions/16139306/determine-season-given-timestamp-in-python-using-datetime
        year = today.year
        month = today.month * 100
        day = today.day
        monthday = month + day

        if monthday >= 921 and monthday <= 1231:
            season = self.SEASONS.index("Fall")
        elif monthday >= 11 and monthday <= 320:
            season = self.SEASONS.index("Winter")
        elif monthday >= 321 and monthday <= 620:
            season = self.SEASONS.index("Spring")
        elif monthday >= 621 and monthday <= 920:
            season = self.SEASONS.index("Summer")
        else:
            season = None

        if season:
            try:
                return Term.objects.get(season_index=season, year=year)
            except Term.DoesNotExist:
                pass

        return None

    class Meta:
        unique_together = ("season_index", "year")
