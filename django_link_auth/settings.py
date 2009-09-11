from django.conf import settings as s
from django.utils.translation import ugettext_lazy as _

# Link's lifetime in seconds. Default - 15 minutes
AUTH_LINK_LIFETIME = getattr(s,
    'AUTH_LINK_LIFETIME', 60 * 15)

# Title for letter with auth link
LINK_AUTH_EMAIL_TITLE = getattr(s,
    'LINK_AUTH_EMAIL_TITLE', _('Auth link from %(domain)s'))

# 'From' field for email with auth link
LINK_AUTH_EMAIL_FROM = getattr(s,
    'LINK_AUTH_EMAIL_FROM', _('noreply@%(domain)s'))

