"""
.. module:: poly_schedules.core.admin
   :synopsis: Poly Schedules Core Admin.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.exceptions import ValidationError
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import PolySchedulesUser

User = get_user_model()


class PolySchedulesUserCreationForm(UserCreationForm):
    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(self.error_messages['duplicate_username'])

    class Meta(UserCreationForm.Meta):
        model = User


class PolySchedulesUserAdmin(UserAdmin):
    add_form = PolySchedulesUserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Instructor info'), {'fields': ('is_instructor', 'is_active_instructor', 'max_wtu', 'course_preferences', 'time_preference', 'preferences_locked')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(PolySchedulesUser, PolySchedulesUserAdmin)
