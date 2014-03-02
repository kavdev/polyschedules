"""
.. module:: poly_schedules.core.ajax
   :synopsis: Poly Schedules Core AJAX Methods.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from ..schedules.models import Term


@dajaxice_register
def update_selected_term(request, term_id, location):
    """ Updates the intructor's course preferences.

    :param term_id: The id of the term to set.
    :type term_id: str

    """

    dajax = Dajax()

    request.session['term_id'] = Term.objects.get(id=term_id).id
    dajax.redirect(location)

    return dajax.json()
