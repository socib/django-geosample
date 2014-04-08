from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datetime import datetime

import models


class PhenomenonObservationUpdateForm(forms.ModelForm):
    button_prefix = _("Update")

    class Meta:
        model = models.PhenomenonObservation
        fields = [
            'phenomenon_type',
            'date_observed',
            'position',
            'some_value',
            'remarks',
        ]

    def clean(self):
        cleaned_data = super(PhenomenonObservationUpdateForm, self).clean()
        # Put here some validation logic
        return cleaned_data

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-5'
        submit_button = Submit(
            css_class='btn btn-primary',
            name='observation',
            value=_('%s PhenomenonObservation') % self.button_prefix,
            type='submit')
        cancel_button = Submit(
            css_class='btn',
            name='cancel',
            value=_('Cancel'),
            type='submit')

        self.helper.add_input(submit_button)
        self.helper.add_input(cancel_button)

        super(PhenomenonObservationUpdateForm, self).__init__(*args, **kwargs)
        self.fields['date_observed'].widget.format = '%d/%m/%Y'
        self.fields['date_observed'].input_formats = ['%d/%m/%Y']
        self.fields['date_observed'].initial = datetime.today()
        self.fields['remarks'].widget.attrs['rows'] = 4
        self.fields['position'].widget.attrs['map_width'] = 450
        self.fields['position'].widget.attrs['num_zoom'] = 5
        self.fields['position'].initial = 'POINT(2.58 39.50)'


class PhenomenonObservationCreateForm(PhenomenonObservationUpdateForm):

    button_prefix = _("Create")

    def __init__(self, *args, **kwargs):
        super(PhenomenonObservationCreateForm, self).__init__(*args, **kwargs)


class PhenomenonObservationFilterForm(forms.Form):

    phenomenon_type = forms.ModelChoiceField(
        models.PhenomenonType.objects.all(),
        label=_('phenomenon type'),
        empty_label='Type: all',
        required=False)
    created_by = forms.ModelChoiceField(
        User.objects.all(),
        label=_('created by'),
        empty_label='User: all',
        required=False)
    source = forms.MultipleChoiceField(
        models.PhenomenonObservation.SOURCE_CHOICES, label=_('source'), required=False)
    from_date = forms.DateField(label=_('from date'), required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'GET'
        filter_button = Submit(
            'filter',
            css_class='btn btn-default',
            value=_('Filter'),
            type='submit')
        self.helper.add_input(filter_button)

        user = kwargs.pop('user')
        super(PhenomenonObservationFilterForm, self).__init__(*args, **kwargs)
        self.fields['from_date'].widget.format = '%d/%m/%Y'
        self.fields['from_date'].input_formats = ['%d/%m/%Y']
        if not user.has_perm('data.can_list_others_phenomenonobservations'):
            self.fields['created_by'].queryset = User.objects.filter(
                id__in=[user.id])

        for key in self.fields:
            self.fields[key].label = self.fields[key].label.capitalize()
