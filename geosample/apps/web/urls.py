from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    'geosample.apps.web.views',
    url(r'^$',
        views.HomePageView.as_view(),
        name='web_home',
        ),
    url(r'^observations/$',
        views.ObservationListView.as_view(),
        name='web_observation_list',
        ),
    # catch all
    url(r'^(?P<url>.*)$',
        views.GenericPageView.as_view(),
        name='web_page',
        ),
)
