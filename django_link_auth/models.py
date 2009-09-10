import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Hash( models.Model ):
    email = models.CharField( _('Email'), max_length = 40)
    hash = models.CharField(_('Hash'), max_length=32)
    next = models.CharField(_('Next'), max_length=255)
    created_at = models.DateTimeField(
        _('Date and time'),
        editable = False,
        default = lambda: datetime.datetime.utcnow(),
    )


    def __unicode__(self):
        return 'Hash for %s' % self.email

