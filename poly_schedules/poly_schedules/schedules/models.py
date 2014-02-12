"""
.. module:: poly_schedules.schedules.models
   :synopsis: Poly Schedules Schedule Models.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

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
    avaialability = ManyToManyField('Day')


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
    SEASON_CHOICES = [(SEASONS.index(day), day) for day in SEASONS]

    season_index = IntegerField(choices=SEASON_CHOICES)
    year = IntegerField()
    schedule = ForeignKey(Schedule)
    available_sections = ManyToManyField(Section)
    preferences_locked = BooleanField()
    votes_locked = BooleanField()
