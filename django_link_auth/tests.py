import datetime

from pdb import set_trace
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from django_link_auth.signals import hash_was_generated

_real_dt = datetime.datetime

def _keep_dt(dt):
    if isinstance(dt, _real_dt):
        return mock_datetime(*dt.timetuple()[:7])
    return dt

class mock_datetime(_real_dt):
    _utcnow = None

    @classmethod
    def freeze(cls):
        cls._utcnow = _keep_dt(_real_dt.utcnow())

    @classmethod
    def goto_future(cls, hours = 0, minutes = 0, seconds = 0):
        if cls._utcnow is None:
            cls.freeze()
        cls._utcnow += datetime.timedelta(0,
            (hours * 60 + minutes) * 60 + seconds)

    @classmethod
    def utcnow(cls):
        if cls._utcnow is None:
            return _keep_dt(_real_dt.utcnow())
        return cls._utcnow

    def __sub__(self, other):
        return _keep_dt(_real_dt.__sub__(self, other))

    def __add__(self, other):
        return _keep_dt(_real_dt.__add__(self, other))

def mock_dt():
    datetime.datetime = mock_datetime

def real_dt():
    datetime.datetime = _real_dt

class LinkAuth(TestCase):
    urls = 'django_link_auth.test_urls'

    def setUp(self):
        mock_dt()
        super(LinkAuth, self).setUp()

    def tearDown(self):
        real_dt()
        super(LinkAuth, self).tearDown()


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
        self.assert_('hash' in kw[0])
        self.assertEqual('svetlyak.40wt@gmail.com', kw[0]['email'])


    def testLogin(self):
        c = Client()
        kw = [None]

        def handler(sender, **kwargs):
            kw[0] = kwargs
        hash_was_generated.connect(handler)

        r = c.post('/send-link/', data = dict(email = 'svetlyak.40wt@gmail.com'))
        self.assertEqual(True, c.login(hash = kw[0]['hash']))


    def testLoginViaExpiredLink(self):
        c = Client()
        kw = [None]

        def handler(sender, **kwargs):
            kw[0] = kwargs
        hash_was_generated.connect(handler)

        r = c.post('/send-link/', data = dict(email = 'svetlyak.40wt@gmail.com'))

        datetime.datetime.goto_future(minutes = 10)
        self.assertEqual(True, c.login(hash = kw[0]['hash']))

        datetime.datetime.goto_future(minutes = 20)
        self.assertEqual(False, c.login(hash = kw[0]['hash']))


    def testMockDt(self):
        datetime.datetime.freeze()
        t1 = datetime.datetime.utcnow()

        datetime.datetime.goto_future(seconds = 900)
        t2 = datetime.datetime.utcnow()

        self.assertEqual(
            datetime.timedelta(0, 900),
            t2 - t1
        )

