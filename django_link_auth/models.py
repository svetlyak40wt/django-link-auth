import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_link_auth.settings import AUTH_LINK_LIFETIME
from django_link_auth.utils import utcnow


class ValidHashManager(models.Manager):
    def get_query_set(self):
        return super(ValidHashManager, self) \
            .get_query_set().filter(
                created_at__gte = utcnow() - \
                                  datetime.timedelta(0, AUTH_LINK_LIFETIME)
            )



class ExpiredHashManager(models.Manager):
    def get_query_set(self):
        return super(ExpiredHashManager, self) \
            .get_query_set().filter(
                created_at__lt = utcnow() - \
                                  datetime.timedelta(0, AUTH_LINK_LIFETIME)
            )



class Hash(models.Model):
    email = models.CharField( _('Email'), max_length = 40)
    hash = models.CharField(_('Hash'), max_length=32)
    next = models.CharField(_('Next'), max_length=255)
    created_at = models.DateTimeField(
        _('Date and time'),
        editable = False,
        default = lambda: utcnow(),
    )

    valid = ValidHashManager()
    expired = ExpiredHashManager()


    def __unicode__(self):
        return 'Hash for %s' % self.email

