from django.conf.urls.defaults import *
from django_link_auth.signals import hash_was_generated
from django_link_auth.utils import send_link_by_email


urlpatterns = patterns('django_link_auth.views',
     (r'^send-login-link/$', 'send_login_link', {}, 'link-auth-send'),
     (r'^login/$', 'login', {}, 'link-auth-login'),
)

hash_was_generated.connect(send_link_by_email)

