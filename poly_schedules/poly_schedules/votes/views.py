"""
.. module:: poly_schedules.votes.views
   :synopsis: Poly Schedules Student Voting Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.http.response import HttpResponseRedirect

from extra_views.formsets import ModelFormSetView

from ..schedules.models import Term
from .models import Vote

MAX_VOTES = 6


class VotesView(ModelFormSetView):

    model = Vote
    template_name = 'votes/votes.html'
    fields = ('course', )
    extra = 1
    max_num = MAX_VOTES
    can_delete = True

    def get_queryset(self):
        return Vote.objects.filter(student=self.request.user, term__id=self.request.session['term_id'])

    def get_context_data(self, **kwargs):
        context = super(VotesView, self).get_context_data(**kwargs)

        term = Term.objects.get(id=self.request.session['term_id'])

        context['max_votes'] = MAX_VOTES
        context['votes_lock_date'] = term.votes_lock_date
        context['votes_locked'] = term.votes_locked

        return context

    def formset_valid(self, formset):
        self.object_list = formset.save(commit=False)

        for object_ in self.object_list:
            object_.student = self.request.user
            object_.term = Term.objects.get(id=self.request.session['term_id'])
            object_.save()

        return HttpResponseRedirect(self.get_success_url())
