from django.forms import CheckboxInput
from django_filters import filters, FilterSet
from apps.tasks.models import Task
from apps.statuses.models import Status
from apps.labels.models import Label
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


class TaskFilter(FilterSet):
    status = filters.ModelChoiceFilter(queryset=Status.objects.all(),
                                       label=_('Status'))
    executor = filters.ModelChoiceFilter(queryset=get_user_model().objects.all(),
                                         label=_('Executor'))
    labels = filters.ModelChoiceFilter(queryset=Label.objects.all(),
                                       label=_('Label'))
    my_tasks = filters.BooleanFilter(
        field_name='creator',
        method='filter_my_tasks',
        label=_('Only your own tasks'),
        widget=CheckboxInput()
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'my_tasks']

    def filter_my_tasks(self, queryset, name, value):
        if value:
            return queryset.filter(creator=self.request.user)
        return queryset
