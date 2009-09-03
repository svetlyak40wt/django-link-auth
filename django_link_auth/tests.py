from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from django_link_auth.signals import hash_was_generated


class LinkAuth(TestCase):
    urls = 'django_link_auth.test_urls'

    def testUrls(self):
        self.assertEqual('/send-link/', reverse('auth-send-link'))
        self.assertEqual('/login/', reverse('login-by-hash'))

    def testGetsNotAllowed(self):
        c = Client()
        self.assertEqual(405, c.get('/send-link/').status_code)
        self.assertEqual(405, c.get('/login/').status_code)

    def testPostEmailRaisesSignal(self):
        c = Client()
        kw = [None]

        def handler(sender, **kwargs):
            kw[0] = kwargs
        hash_was_generated.connect(handler)

        r = c.post('/send-link/', data = dict(email = 'svetlyak.40wt@gmail.com'))

        self.assert_(kw[0] is not None)

