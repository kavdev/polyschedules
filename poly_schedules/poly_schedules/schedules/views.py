"""
.. module:: resnet_internal.portmap.views
   :synopsis: ResNet Internal Residence Halls Port Map Views.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.generic import TemplateView

from django_datatables_view.base_datatable_view import BaseDatatableView

from .models import Term, SectionTime


class BaseScheduleView(TemplateView):
    template_name = "schedules/schedule.html"

    def get_context_data(self, **kwargs):
        context = super(BaseScheduleView, self).get_context_data(**kwargs)
        context["populate_url"] = reverse("populate_base_schedule")

        return context


class PopulateBaseSchedule(BaseDatatableView):
    """Renders the schedule."""

    def get_initial_queryset(self):
        return Term().get_or_create_current_term().schedule.sections.all().select_related()

    # define the columns that will be returned
    columns = ['id', 'course', 'number', 'instructor', 'location', 'times', 'is_lab', 'course.units', 'course.wtu']

    # define column names that can be sorted
    order_columns = columns

    # define columns that can be searched
    searchable_columns = ['course__prefix', 'course__number', 'course__units', 'course__wtu', 'number', 'instructor__first_name',
                          'instructor__last_name', 'instructor__username', 'location__building',
                          'location__building_number', 'location__room_number', 'times__time_pattern', 'times__start_time', 'is_lab']

    # define columns that can be edited
    editable_columns = []

    def render_column(self, row, column):
        """Render columns with customized HTML.

        :param row: A dictionary containing row data.
        :type row: dict
        :param column: The name of the column to be rendered. This can be used to index into the row dictionary.
        :type column: str
        :returns: The HTML to be displayed for this column.

        """

        # Attempt to follow relationships
        try:
            text = getattr(row, column)
        except AttributeError:
            obj = row
            for part in column.split('.'):
                if obj is None:
                    break
                obj = getattr(obj, part)

            text = obj

        if column == 'times':
            return "<div id='%s' column='%s'>%s</div>" % (row.id, column, "\n".join([str(time) for time in getattr(row, column).all()]))
        if column == 'is_lab':
            return "<div id='%s' column='%s'>%s</div>" % (row.id, column, "Lab" if getattr(row, column) else "Lec")
        else:
            return "<div id='%s' column='%s'>%s</div>" % (row.id, column, text)

    def filter_queryset(self, qs):
        """ Filters the QuerySet by submitted search parameters.

        Made to work with multiple word search queries.
        PHP source: http://datatables.net/forums/discussion/3343/server-side-processing-and-regex-search-filter/p1
        Credit for finding the Q.AND method: http://bradmontgomery.blogspot.com/2009/06/adding-q-objects-in-django.html

        :param qs: The QuerySet to be filtered.
        :type qs: QuerySet
        :returns: If search parameters exist, the filtered QuerySet, otherwise the original QuerySet.

        """

        search_parameters = self.request.GET.get('sSearch', None)

        if search_parameters:
            params = search_parameters.split(" ")

            columnQ = None
            paramQ = None
            firstCol = True
            firstParam = True

            for param in params:
                if param != "":
                    for searchable_column in self.searchable_columns:
                        # Handle is_lab column
                        if searchable_column == 'is_lab' and (param.lower() == 'lab' or param.lower() == 'lec'):
                            kwargz = {"is_lab": (True if param.lower() == 'lab' else False)}
                        # Handle time patterns
                        elif searchable_column == 'times__time_pattern' and param.upper() in SectionTime.TIME_PATTERNS:
                            kwargz = {"times__time_pattern": SectionTime.TIME_PATTERNS.index(param.upper())}
                        else:
                            kwargz = {searchable_column + "__icontains": param}
                        q = Q(**kwargz)
                        if (firstCol):
                            firstCol = False
                            columnQ = q
                        else:
                            columnQ |= q
                    if (firstParam):
                        firstParam = False
                        paramQ = columnQ
                    else:
                        paramQ.add(columnQ, Q.AND)
                    columnQ = None
                    firstCol = True
            qs = qs.filter(paramQ)

        return qs
