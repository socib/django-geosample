# coding: utf-8
from geosample.apps.web.views import BasePageView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, DeleteView
from django_tables2.views import SingleTableView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.exceptions import PermissionDenied
import models
import forms
import tables


class PhenomenonObservationMixin(BasePageView):
    """
    Shared code for create or update a PhenomenonObservation
    """

    model = models.PhenomenonObservation

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PhenomenonObservationMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PhenomenonObservationMixin, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(PhenomenonObservationMixin, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PhenomenonObservationMixin, self).get_form_kwargs()
        return kwargs

    def get_initial(self):
        initial = super(PhenomenonObservationMixin, self).get_initial()
        initial = initial.copy()
        # initial[''] =
        return initial

    def get_success_url(self):
        return reverse('data_observation_list')


class PhenomenonObservationCreate(PhenomenonObservationMixin, CreateView):
    """
    Create a new Phenomenon Observation
    """

    template_name_suffix = '_create'
    form_class = forms.PhenomenonObservationCreateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.source = models.PhenomenonObservation.WEBFORM
        self.object.save(user=self.request.user)
        # Notify that in messages area
        messages.add_message(self.request, messages.SUCCESS, _('Observation created'))
        return super(PhenomenonObservationCreate, self).form_valid(form)


class PhenomenonObservationUpdate(PhenomenonObservationMixin, UpdateView):
    """
    Update Phenomenon Observation
    """

    template_name_suffix = '_update'
    form_class = forms.PhenomenonObservationUpdateForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save(user=self.request.user)
        # Notify that in messages area
        messages.add_message(self.request, messages.SUCCESS, _('Observation updated'))
        return super(PhenomenonObservationUpdate, self).form_valid(form)


class PhenomenonObservationDelete(PhenomenonObservationMixin, DeleteView):
    """
    Delete an observation
    """

    template_name_suffix = '_delete'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('data.delete_phenomenonobservation'):
            raise PermissionDenied()
        return super(PhenomenonObservationDelete, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Override delete method to send user
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        messages.add_message(self.request, messages.SUCCESS, _('Observation deleted'))
        self.object.delete(user=self.request.user)
        return HttpResponseRedirect(success_url)


class PhenomenonObservationList(BasePageView, SingleTableView):
    """
    List observations
    """

    table_class = tables.PhenomenonObservationTable
    model = models.PhenomenonObservation
    table_pagination = {"per_page": 50}

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.has_perm('data.can_list_phenomenonobservations'):
            raise PermissionDenied()
        self.form = forms.PhenomenonObservationFilterForm(self.request.GET,
                                                          user=request.user)
        return super(PhenomenonObservationList, self).dispatch(request, *args, **kwargs)

    def get_table_data(self):
        data = models.PhenomenonObservation.objects.all()
        user = self.request.user

        # Filter observations
        if not user.is_superuser and not user.is_staff:
            data = data.filter(created_by=user)

        if self.form.is_valid():
            if self.form.cleaned_data['phenomenon_type']:
                data = data.filter(
                    phenomenon_type=self.form.cleaned_data['phenomenon_type'])
            if self.form.cleaned_data.get('created_by'):
                data = data.filter(
                    created_by=self.form.cleaned_data['created_by'])
            if self.form.cleaned_data.get('source'):
                data = data.filter(
                    source=self.form.cleaned_data['source'])
            if self.form.cleaned_data.get('from_date'):
                data = data.filter(
                    date_observed__gte=self.form.cleaned_data['from_date'])
        data = data.order_by('-date_observed')
        return data

    def get_context_data(self, **kwargs):
        context = super(PhenomenonObservationList, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context
