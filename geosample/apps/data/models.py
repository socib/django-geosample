from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class PhenomenonType(models.Model):
    code = models.CharField(_('code'), max_length=20, unique=True)
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'))
    # Audit
    created_on = models.DateTimeField(_('date added'), auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='created-pt')
    updated_on = models.DateTimeField(_('date modified'), auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='updated-pt')

    def __unicode__(self):
        return "{code} - {name}".format(code=self.code, name=self.name)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.id:
            self.created_by = user
        return super(PhenomenonType, self).save(*args, **kwargs)


class PhenomenonObservation(models.Model):
    WEBFORM, API, BULK = ('W', 'A', 'B')
    SOURCE_CHOICES = (
        (WEBFORM, _('Web Form')),
        (API, _('API')),
        (BULK, _('Bulk upload')),
    )

    phenomenon_type = models.ForeignKey(PhenomenonType, on_delete=models.PROTECT)
    date_observed = models.DateTimeField(_('date observed'))
    position = models.PointField(srid=4326)
    source = models.CharField(_('source'), max_length=2,
                              choices=SOURCE_CHOICES,
                              default=WEBFORM, blank=False)
    some_value = models.IntegerField('some value')
    remarks = models.TextField(_('remarks'), blank=True, null=True)
    # Audit
    created_on = models.DateTimeField(_('date added'), auto_now_add=True)
    created_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='created-po')
    updated_on = models.DateTimeField(_('date modified'), auto_now=True)
    updated_by = models.ForeignKey(User, blank=True, null=True,
                                   editable=False, related_name='updated-po')

    objects = models.GeoManager()

    class Meta:
        permissions = (
            ("can_list_phenomenonobservations",
             "Can list phenomenon observations"),
            ("can_list_others_phenomenonobservations",
             "Can list phenomenon observations from others"),
        )

    def __unicode__(self):
        return "{type} on {date:%d/%m/%Y}".format(
            type=self.phenomenon_type.name,
            date=self.date_observed)

    def save(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        self.updated_by = user
        if not self.id:
            self.created_by = user
        return super(PhenomenonObservation, self).save(*args, **kwargs)
