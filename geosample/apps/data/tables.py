import django_tables2 as tables
from django_tables2.utils import A
import models


class PhenomenonObservationTable(tables.Table):
    phenomenon_type = tables.LinkColumn('data_observation_update', args=[A('pk')])
    date_observed = tables.DateColumn(format='d/m/Y')
    # position = tables.Column()
    position = tables.TemplateColumn('{{ record.position.x }} {{ record.position.y }}')
    source = tables.Column()
    some_value = tables.Column()
    created_by = tables.Column()

    class Meta:
        model = models.PhenomenonObservation
        attrs = {"class": "table table-striped"}
        sequence = fields = (
            'phenomenon_type',
            'date_observed',
            'position',
            'source',
            'some_value',
            'created_by',
        )
