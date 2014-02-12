"""
.. module:: poly_schedules.schedules.fields
   :synopsis: Poly Schedules Schedules Custom Model Fields.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""
from django.db.models import TextField, SubfieldBase


class BooleanListField(TextField):
    __metaclass__ = SubfieldBase
    description = "Stores an array of booleans"

    def __init__(self, *args, **kwargs):
        super(BooleanListField, self).__init__(*args, **kwargs)

    def to_python(self, value):

        if not value:
            value = []

        if isinstance(value, list):
            return value

        return map(bool, map(int, list(value)))

    def get_prep_value(self, value):
        if value is None:
            return value

        return unicode(''.join(map(str, map(int, value))))

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

# Lets South know that this custom field is okay
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^schedules\.fields\.BooleanListField"])
