from django.conf.urls.defaults import *

urlpatterns = patterns('',
     (r'', include('django_link_auth.urls')),
)

