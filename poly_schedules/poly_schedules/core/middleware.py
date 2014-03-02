"""
.. module:: poly_schedules.core.middleware
   :synopsis: Poly Schedules Core Middleware.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from ..schedules.models import Term


class TermMiddleware(object):
    """Adds the current term to the session if the session variable doesn't already exist"""

    def process_request(self, request):
        if 'term_id' not in request.session:
            request.session['term_id'] = Term().get_or_create_current_term().id
