import datetime
import re

from pdb import set_trace

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend

from django_link_auth.models import Hash

# Link's lifetime in seconds. Default - 15 minutes
AUTH_LINK_LIFETIME = getattr(settings, 'AUTH_LINK_LIFETIME', 60 * 15)

class LinkBackend(ModelBackend):
    def authenticate(self, hash = None):
        try:
            hash = Hash.objects.get(
                hash = hash,
                created_at__gte = datetime.datetime.utcnow() - \
                                  datetime.timedelta(0, AUTH_LINK_LIFETIME)
            )
        except Hash.DoesNotExist:
            return None

        try:
            user = User.objects.get(email = hash.email)
        except User.DoesNotExist:
            user = User(
                email = hash.email,
                username = re.sub('[.@]', '-', hash.email)
            )
            user.save()
        return user

