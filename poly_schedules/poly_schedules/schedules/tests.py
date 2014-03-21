"""
.. module:: poly_schedules.schedules.tests
   :synopsis: Poly Schedules Schedule Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

import datetime

from django.utils import unittest

from .fields import BooleanListField
from poly_schedules.schedules.models import Term


class BooleanListFieldTest(unittest.TestCase):
    """Tests the conversion methods of the BooleanListField."""

    def setUp(self):
        self.field = BooleanListField()
        self.string_value = "1010101000100100100100001001001010"
        self.list_value = [True, False, True, False, True, False, True, False, False, False, True, False, False, True, False, False, True, False, False, True, False, False, False, False, True, False, False, True, False, False, True, False, True, False]

    def test_to_python(self):
        self.assertEqual(self.list_value, self.field.to_python(self.string_value))
        self.assertEqual([], self.field.to_python(None))
        self.assertEqual(["Yo"], self.field.to_python(["Yo"]))

        # should raise an exception for an immutable sequence
        self.assertRaises(ValueError, self.field.to_python, "characters")

    def test_get_prep_value(self):
        self.assertEqual(self.string_value, self.field.get_prep_value(self.list_value))
        self.assertEqual(None, self.field.get_prep_value(None))

        # should raise an exception for an immutable sequence
        self.assertRaises(ValueError, self.field.get_prep_value, ["c", 1, None])

    def test_conversion(self):
        self.assertEqual(self.string_value, self.field.get_prep_value(self.field.to_python(self.string_value)), "Failed to convert data to List and back to String")
        self.assertEqual(self.list_value, self.field.to_python(self.field.get_prep_value(self.list_value)), "Failed to convert data to String and back to List")


class TermMethodsTest(unittest.TestCase):
    """Tests the Term model methods."""

    def setUp(self):
        self.term = Term().get_or_create_current_term()
        self.today = datetime.date.today()

    def test_preferences_locked(self):
        if self.today >= self.term.preferences_lock_date:
            self.assertEqual(True, self.term.preferences_locked)
        else:
            self.assertEqual(False, self.term.preferences_locked)

    def test_votes_locked(self):
        if self.today >= self.term.votes_lock_date:
            self.assertEqual(True, self.term.votes_locked)
        else:
            self.assertEqual(False, self.term.votes_locked)

            