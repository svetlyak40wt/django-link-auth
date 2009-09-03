from django.conf.urls.defaults import *

urlpatterns = patterns('django_link_auth.views',
     (r'^send-link/$', 'send_link', {}, 'auth-send-link'),
     (r'^login/$', 'login', {}, 'login-by-hash'),
)

