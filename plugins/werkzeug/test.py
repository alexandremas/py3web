import unittest
import os
import py3web
from py3web.ext import werkzeug as bw

class WerkzeugTest(unittest.TestCase):
    def setUp(self):
        self.app = py3web.Bottle(catchall=False)
        self.plugin = self.app.install(bw.WerkzeugPlugin())

    def test_resquest_obj(self):
        request = self.plugin.request
        @self.app.get('/')
        def test():
            self.assertEqual(request.environ, py3web.request.environ)
            self.assertNotEqual(request, py3web.request)
            self.assertEqual(request.accept_languages.best, 'de')
            return repr(self.plugin.request)
        self.app({'PATH_INFO':'/', 'REQUEST_METHOD':'GET',
                  'HTTP_ACCEPT_LANGUAGE': 'de, en;q=0.7'}, lambda x, y: None)

if __name__ == '__main__':
    unittest.main()
