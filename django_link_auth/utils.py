import datetime
import pytz

from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from django_link_auth.settings import \
    AUTH_LINK_LIFETIME, \
    LINK_AUTH_EMAIL_TITLE, \
    LINK_AUTH_EMAIL_FROM

def send_link_by_email(sender, email, hash, **kwargs):
    site = Site.objects.get_current()

    params = dict(
        domain = site, site_name = site.name, hash = hash,
        expire_at = pytz.utc.localize(datetime.datetime.utcnow()) + \
                    datetime.timedelta(0, AUTH_LINK_LIFETIME)
    )

    email_body = render_to_string('email/auth_link.html', params)

    send_mail(LINK_AUTH_EMAIL_TITLE % params,
              email_body,
              LINK_AUTH_EMAIL_FROM % params,
              (email,)
    )

