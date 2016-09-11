from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^scan$', 'tutorons.packages.views.scan', name='package_scan'),
    url(r'^explain$', 'tutorons.packages.views.explain', name='package_explain'),
)
