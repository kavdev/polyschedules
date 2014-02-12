"""
.. module:: poly_schedules.schedules.tests
   :synopsis: Poly Schedules Schedule Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.utils import unittest

from .fields import BooleanListField


class BooleanListFieldTest(unittest.TestCase):
    """Tests the conversion methods of the BooleanListField."""

    def setUp(self):
        self.field = BooleanListField()
        self.stringValue = "1010101000100100100100001001001010"
        self.listValue = [True, False, True, False, True, False, True, False, False, False, True, False, False, True, False, False, True, False, False, True, False, False, False, False, True, False, False, True, False, False, True, False, True, False]

    def test_to_python(self):
        self.assertEqual(self.listValue, self.field.to_python(self.stringValue))

        # should raise an exception for an immutable sequence
        self.assertRaises(ValueError, self.field.to_python, "characters")

    def test_get_prep_value(self):
        self.assertEqual(self.stringvalue, self.field.get_prep_value(self.listValue))

        # should raise an exception for an immutable sequence
        self.assertRaises(ValueError, self.field.get_prep_value, ["c", 1, None])

    def test_conversion(self):
        self.assertEqual(self.stringValue, self.field.get_prep_value(self.field.to_python(self.stringValue)), "Failed to convert data to List and back to String")
        self.assertEqual(self.listValue, self.field.to_python(self.field.get_prep_value(self.listValue)), "Failed to convert data to String and back to List")
