from django.db import models
from django.utils.translation import ugettext_lazy as _

class Hash( models.Model ):
    email = models.CharField( _('Email'), max_length = 40, unique = True)
    hash = models.CharField(_('Hash'), max_length=32, unique = True)

    def __unicode__(self):
        return 'Hash for %s' % self.email

