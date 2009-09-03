from django.test import TestCase
from django.core.urlresolvers import reverse


class LinkAuth(TestCase):
    urls = 'django_link_auth.test_urls'

    def testUrls(self):
        self.assertEqual('/send-link/', reverse('auth-send-link'))
        self.assertEqual('/login/', reverse('login-by-hash'))
