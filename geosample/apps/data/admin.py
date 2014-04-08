from django.contrib.gis import admin
from models import PhenomenonType, PhenomenonObservation


class PhenomenonTypeAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', 'updated_by',)

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)


class PhenomenonObservationAdmin(admin.GeoModelAdmin):
    readonly_fields = ('created_by', 'updated_by',)
    openlayers_url = 'js/open_layers/OpenLayers.js'
    default_lon = 2.58
    default_lat = 39.50
    default_zoom = 9

    def save_model(self, request, obj, form, change):
        obj.save(user=request.user)

admin.site.register(PhenomenonType, PhenomenonTypeAdmin)
admin.site.register(PhenomenonObservation, PhenomenonObservationAdmin)
