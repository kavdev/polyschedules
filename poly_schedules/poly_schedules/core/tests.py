"""
.. module:: poly_schedules.core.tests
   :synopsis: Poly Schedules Core Tests.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.utils import unittest
from django.contrib.auth import get_user_model
from poly_schedules.schedules.models import Term, Course


class UserMethodsTest(unittest.TestCase):
    """Tests the get name/alias methods of the user model."""

    def setUp(self):
        first_name = "Alexander"
        last_name = "Kavanaugh"
        input_alias = "akavanau-admin"
        self.full_name = "Alexander Kavanaugh"
        self.alias = "akavanau"
        self.user, created = get_user_model().objects.get_or_create(username=input_alias)

        if created:
            self.user.first_name = first_name
            self.user.last_name = last_name
            self.user.is_superuser = True
            self.user.save()

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), self.full_name)

    def test_get_alias(self):
        self.assertEqual(self.user.get_alias(), self.alias)

    def test_initialize_preferences(self):
        term_id = Term().get_or_create_current_term().id

        new_course = Course()
        new_course.prefix = "TEST"
        new_course.number = 101
        new_course.title = "Introduction to Testing"
        new_course.save()

        self.user.initialize_preferences(term_id)
