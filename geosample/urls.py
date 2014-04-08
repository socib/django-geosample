from django.conf.urls.static import static
from django.conf.urls import patterns, url, include
from django.conf import settings

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    # (r'', include('geosample.apps.')),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^data/', include('geosample.apps.data.urls')),
    (r'^login/?$', 'django.contrib.auth.views.login'),
    (r'^logout/?$', 'django.contrib.auth.views.logout', {'next_page': '/login'}),
    (r'^', include('geosample.apps.web.urls')),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
