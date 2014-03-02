"""
.. module:: poly_schedules.preferences.ajax
   :synopsis: Poly Schedules Preferences AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register


@dajaxice_register
def update_course_preference(request, course_id, preference):
    """ Updates the intructor's course preferences.

    :param course_id: The id of the toner cartridge to process.
    :type course_id: str
    :param preference: The updated preference.
    :type preference: str

    """

    dajax = Dajax()

    # Get the preference in question
    preference_instance = request.user.course_preferences.select_related().get(term__id=request.session['term_id'], course=course_id)
    preference_instance.preference = int(preference)
    preference_instance.save()

    return dajax.json()


@dajaxice_register
def update_time_preference(request, day, hour):
    """ Updates the intructor's time preference.

    :param day: The day to process.
    :type course_id: str
    :param preference: The hour to process.
    :type preference: str

    """

    dajax = Dajax()

    availability = request.user.time_preference.select_related().get(term__id=request.session['term_id']).availability

    # Modify the hours list
    hour = int(hour)
    hours_list = getattr(availability, day)
    hours_list[hour] = not hours_list[hour]

    # Attach the new list to the week
    setattr(availability, day, hours_list)
    availability.save()

    return dajax.json()
