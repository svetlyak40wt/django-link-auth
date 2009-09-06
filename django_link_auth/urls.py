from django.conf.urls.defaults import *

urlpatterns = patterns('django_link_auth.views',
     (r'^send-login-link/$', 'send_login_link', {}, 'send-login-link'),
)

