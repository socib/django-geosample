from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    'geosample.apps.data.views',
    url(r'^observation/create/?$',
        views.PhenomenonObservationCreate.as_view(),
        name='data_observation_create',
        ),
    url(r'^observation/(?P<pk>\d+)/update/?$',
        views.PhenomenonObservationUpdate.as_view(),
        name='data_observation_update',
        ),
    url(r'^observation/(?P<pk>\d+)/delete/?$',
        views.PhenomenonObservationDelete.as_view(),
        name='data_observation_delete',
        ),
    url(r'^observation/list/?$',
        views.PhenomenonObservationList.as_view(),
        name='data_observation_list',
        ),
)
