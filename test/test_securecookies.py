#coding: utf-8
import unittest

import py3web
from py3web import tob, touni

class TestSecureCookies(unittest.TestCase):
    def setUp(self):
        self.data = dict(a=5, b=touni('υηι¢σ∂є'), c=[1,2,3,4,tob('bytestring')])
        self.key = tob('secret')

    def testDeEncode(self):
        cookie = py3web.cookie_encode(self.data, self.key)
        decoded = py3web.cookie_decode(cookie, self.key)
        self.assertEqual(self.data, decoded)
        decoded = py3web.cookie_decode(cookie+tob('x'), self.key)
        self.assertEqual(None, decoded)

    def testIsEncoded(self):
        cookie = py3web.cookie_encode(self.data, self.key)
        self.assertTrue(py3web.cookie_is_encoded(cookie))
        self.assertFalse(py3web.cookie_is_encoded(tob('some string')))

class TestSecureCookiesInBottle(unittest.TestCase):
    def setUp(self):
        self.data = dict(a=5, b=touni('υηι¢σ∂є'), c=[1,2,3,4,tob('bytestring')])
        self.secret = tob('secret')
        py3web.app.push()
        py3web.response.bind()

    def tear_down(self):
        py3web.app.pop()

    def get_pairs(self):
        for k, v in py3web.response.headerlist:
            if k == 'Set-Cookie':
                key, value = v.split(';')[0].split('=', 1)
                yield key.lower().strip(), value.strip()
    
    def set_pairs(self, pairs):
        header = ','.join(['%s=%s' % (k, v) for k, v in pairs])
        py3web.request.bind({'HTTP_COOKIE': header})

    def testValid(self):
        py3web.response.set_cookie('key', self.data, secret=self.secret)
        pairs = self.get_pairs()
        self.set_pairs(pairs)
        result = py3web.request.get_cookie('key', secret=self.secret)
        self.assertEqual(self.data, result)

    def testWrongKey(self):
        py3web.response.set_cookie('key', self.data, secret=self.secret)
        pairs = self.get_pairs()
        self.set_pairs([(k+'xxx', v) for (k, v) in pairs])
        result = py3web.request.get_cookie('key', secret=self.secret)
        self.assertEqual(None, result)


if __name__ == '__main__': #pragma: no cover
    unittest.main()
