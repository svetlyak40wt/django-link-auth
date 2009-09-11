import datetime

from pdb import set_trace
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth import \
    SESSION_KEY, \
    BACKEND_SESSION_KEY

from django_link_auth.models import Hash
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
        self.send_login_url = reverse('link-auth-send')
        self.login_url = reverse('link-auth-login')
        mock_dt()
        super(LinkAuth, self).setUp()

    def tearDown(self):
        real_dt()
        super(LinkAuth, self).tearDown()


    def testGetsNotAllowed(self):
        c = Client()
        self.assertEqual(405, c.get(self.send_login_url).status_code)


    def testPostsNotAllowed(self):
        c = Client()
        self.assertEqual(405, c.post(self.login_url).status_code)


    def testPostEmailGeneratesSignal(self):
        c = Client()
        kw = [None]

        def handler(sender, **kwargs):
            kw[0] = kwargs
        hash_was_generated.connect(handler)

        r = c.post(self.send_login_url, data = dict(email = 'svetlyak.40wt@gmail.com'))

        self.assert_(kw[0] is not None)
        self.assert_('hash' in kw[0])
        self.assertEqual('svetlyak.40wt@gmail.com', kw[0]['email'])


    def testLogin(self):
        c = Client()

        self.assertEqual(0, Hash._default_manager.count())

        hash = self.getHash()

        self.assertEqual(True, c.login(hash = hash))
        self.assertEqual(0, Hash._default_manager.count())


    def testLoginViaExpiredLink(self):
        c = Client()
        hash = self.getHash()

        datetime.datetime.goto_future(minutes = 10)
        self.assertEqual(True, c.login(hash = hash))

        datetime.datetime.goto_future(minutes = 20)
        self.assertEqual(False, c.login(hash = hash))


    def testOldHashesExpire(self):
        c = Client()
        hash = self.getHash()

        datetime.datetime.goto_future(minutes = 10)
        self.assertEqual(1, Hash.valid.count())
        self.assertEqual(0, Hash.expired.count())

        datetime.datetime.goto_future(minutes = 20)
        self.assertEqual(0, Hash.valid.count())
        self.assertEqual(1, Hash.expired.count())


    def testMockDt(self):
        datetime.datetime.freeze()
        t1 = datetime.datetime.utcnow()

        datetime.datetime.goto_future(seconds = 900)
        t2 = datetime.datetime.utcnow()

        self.assertEqual(
            datetime.timedelta(0, 900),
            t2 - t1
        )


    def testLoginView(self):
        c = Client()
        referer = 'http://testserver/blah/minor/'
        hash = self.getHash(referer = referer)

        self.assertEqual([], c.session.items())

        r = c.get(self.login_url + '?hash=' + hash)

        self.assertEqual(
            [
                (SESSION_KEY, 1),
                (BACKEND_SESSION_KEY, 'django_link_auth.backends.LinkBackend')
            ],
            c.session.items())
        self.assertEqual(302, r.status_code)
        self.assertEqual(referer, r['Location'])


    def getHash(self, referer = '/'):
        c = Client()
        kw = [None]

        def handler(sender, **kwargs):
            kw[0] = kwargs
        hash_was_generated.connect(handler)

        r = c.post(
            self.send_login_url,
            data = dict(email = 'svetlyak.40wt@gmail.com'),
            HTTP_REFERER = referer,
        )
        return kw[0]['hash']
