from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from tutorons.common.api import ClientQueryResource, ViewResource

v1_api = Api(api_name='v1')
v1_api.register(ClientQueryResource())
v1_api.register(ViewResource())

urlpatterns = patterns(
    '',
    url(r'^$', 'tutorons.views.home', name='home'),
    url(r'^home$', 'tutorons.views.home', name='home'),
    url(r'^wget/', include('tutorons.wget.urls')),
    url(r'^css/', include('tutorons.css.urls')),
    url(r'^python/', include('tutorons.python.urls')),
    url(r'^regex/', include('tutorons.regex.urls')),
    url(r'^packages/', include('tutorons.packages.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
)
