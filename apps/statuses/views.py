from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.statuses.forms import StatusForm
from apps.statuses.models import Status
from django.utils.translation import gettext as _
from django.urls import reverse_lazy
from django.contrib import messages
from task_manager.mixins import CustomLoginRequiredMixin


# Create your views here.
class StatusIndexView(CustomLoginRequiredMixin, ListView):
    template_name = 'apps/statuses/statuses.html'
    model = Status
    context_object_name = 'statuses'


class StatusCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'apps/statuses/create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully created')


class StatusUpdateView(CustomLoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'apps/statuses/update.html'
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully changed')


class StatusDeleteView(CustomLoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'apps/statuses/delete.html'
    success_url = reverse_lazy('statuses')
    success_message = _('The status has been successfully deleted')

    def post(self, request, *args, **kwargs):
        if self.get_object().tasks.exists():
            messages.error(
                self.request,
                _('Unable to delete a status because it is being used'))
            return redirect('statuses')
        return super().post(request, *args, **kwargs)
