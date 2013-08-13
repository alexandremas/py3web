# -*- coding: utf-8 -*-
import unittest
import py3web
from tools import ServerTestBase
from py3web import tob

class TestWsgi(ServerTestBase):
    ''' Tests for WSGI functionality, routing and output casting (decorators) '''

    def test_get(self):
        """ WSGI: GET routes"""
        @py3web.route('/')
        def test(): return 'test'
        self.assertStatus(404, '/not/found')
        self.assertStatus(405, '/', post="var=value")
        self.assertBody('test', '/')

    def test_post(self):
        """ WSGI: POST routes"""
        @py3web.route('/', method='POST')
        def test(): return 'test'
        self.assertStatus(404, '/not/found')
        self.assertStatus(405, '/')
        self.assertBody('test', '/', post="var=value")

    def test_headget(self):
        """ WSGI: HEAD routes and GET fallback"""
        @py3web.route('/get')
        def test(): return 'test'
        @py3web.route('/head', method='HEAD')
        def test2(): return 'test'
        # GET -> HEAD
        self.assertStatus(405, '/head')
        # HEAD -> HEAD
        self.assertStatus(200, '/head', method='HEAD')
        self.assertBody('', '/head', method='HEAD')
        # HEAD -> GET
        self.assertStatus(200, '/get', method='HEAD')
        self.assertBody('', '/get', method='HEAD')

    def test_request_attrs(self):
        """ WSGI: POST routes"""
        @py3web.route('/')
        def test():
            self.assertEqual(py3web.request.app,
                             py3web.default_app())
            self.assertEqual(py3web.request.route,
                             py3web.default_app().routes[0])
            return 'foo'
        self.assertBody('foo', '/')

    def get304(self):
        """ 304 responses must not return entity headers """
        bad = ('allow', 'content-encoding', 'content-language',
               'content-length', 'content-md5', 'content-range',
               'content-type', 'last-modified') # + c-location, expires?
        for h in bad:
            py3web.response.set_header(h, 'foo')
        py3web.status = 304
        for h, v in py3web.response.headerlist:
            self.assertFalse(h.lower() in bad, "Header %s not deleted" % h)

    def test_anymethod(self):
        self.assertStatus(404, '/any')
        @py3web.route('/any', method='ANY')
        def test2(): return 'test'
        self.assertStatus(200, '/any', method='HEAD')
        self.assertBody('test', '/any', method='GET')
        self.assertBody('test', '/any', method='POST')
        self.assertBody('test', '/any', method='DELETE')
        @py3web.route('/any', method='GET')
        def test2(): return 'test2'
        self.assertBody('test2', '/any', method='GET')
        @py3web.route('/any', method='POST')
        def test2(): return 'test3'
        self.assertBody('test3', '/any', method='POST')
        self.assertBody('test', '/any', method='DELETE')

    def test_500(self):
        """ WSGI: Exceptions within handler code (HTTP 500) """
        @py3web.route('/')
        def test(): return 1/0
        self.assertStatus(500, '/')

    def test_500_unicode(self):
        @py3web.route('/')
        def test(): raise Exception(touni('Unicode äöüß message.'))
        self.assertStatus(500, '/')

    def test_utf8_url(self):
        """ WSGI: Exceptions within handler code (HTTP 500) """
        @py3web.route('/my/:string')
        def test(string): return string
        self.assertBody(tob('urf8-öäü'), '/my/urf8-öäü')

    def test_utf8_404(self):
        self.assertStatus(404, '/not-found/urf8-öäü')

    def test_401(self):
        """ WSGI: abort(401, '') (HTTP 401) """
        @py3web.route('/')
        def test(): py3web.abort(401)
        self.assertStatus(401, '/')
        @py3web.error(401)
        def err(e):
            py3web.response.status = 200
            return str(type(e))
        self.assertStatus(200, '/')
        self.assertBody("<class 'bottle.HTTPError'>",'/')

    def test_303(self):
        """ WSGI: redirect (HTTP 303) """
        @py3web.route('/')
        def test(): py3web.redirect('/yes')
        @py3web.route('/one')
        def test2(): py3web.redirect('/yes',305)
        env = {'SERVER_PROTOCOL':'HTTP/1.1'}
        self.assertStatus(303, '/', env=env)
        self.assertHeader('Location', 'http://127.0.0.1/yes', '/', env=env)
        env = {'SERVER_PROTOCOL':'HTTP/1.0'}
        self.assertStatus(302, '/', env=env)
        self.assertHeader('Location', 'http://127.0.0.1/yes', '/', env=env)
        self.assertStatus(305, '/one', env=env)
        self.assertHeader('Location', 'http://127.0.0.1/yes', '/one', env=env)

    def test_generator_callback(self):
        @py3web.route('/yield')
        def test():
            py3web.response.headers['Test-Header'] = 'test'
            yield 'foo'
        @py3web.route('/yield_nothing')
        def test2():
            yield
            py3web.response.headers['Test-Header'] = 'test'
        self.assertBody('foo', '/yield')
        self.assertHeader('Test-Header', 'test', '/yield')
        self.assertBody('', '/yield_nothing')
        self.assertHeader('Test-Header', 'test', '/yield_nothing')

    def test_cookie(self):
        """ WSGI: Cookies """
        @py3web.route('/cookie')
        def test():
            py3web.response.set_cookie('b', 'b')
            py3web.response.set_cookie('c', 'c', path='/')
            return 'hello'
        try:
            c = self.urlopen('/cookie')['header'].get_all('Set-Cookie', '')
        except:
            c = self.urlopen('/cookie')['header'].get('Set-Cookie', '').split(',')
            c = [x.strip() for x in c]
        self.assertTrue('b=b' in c)
        self.assertTrue('c=c; Path=/' in c)


class TestRouteDecorator(ServerTestBase):
    def test_decorators(self):
        def foo(): return py3web.request.method
        py3web.get('/')(foo)
        py3web.post('/')(foo)
        py3web.put('/')(foo)
        py3web.delete('/')(foo)
        for verb in 'GET POST PUT DELETE'.split():
            self.assertBody(verb, '/', method=verb)

    def test_single_path(self):
        @py3web.route('/a')
        def test(): return 'ok'
        self.assertBody('ok', '/a')
        self.assertStatus(404, '/b')

    def test_path_list(self):
        @py3web.route(['/a','/b'])
        def test(): return 'ok'
        self.assertBody('ok', '/a')
        self.assertBody('ok', '/b')
        self.assertStatus(404, '/c')

    def test_no_path(self):
        @py3web.route()
        def test(x=5): return str(x)
        self.assertBody('5', '/test')
        self.assertBody('6', '/test/6')

    def test_no_params_at_all(self):
        @py3web.route
        def test(x=5): return str(x)
        self.assertBody('5', '/test')
        self.assertBody('6', '/test/6')

    def test_method(self):
        @py3web.route(method='gEt')
        def test(): return 'ok'
        self.assertBody('ok', '/test', method='GET')
        self.assertStatus(200, '/test', method='HEAD')
        self.assertStatus(405, '/test', method='PUT')

    def test_method_list(self):
        @py3web.route(method=['GET','post'])
        def test(): return 'ok'
        self.assertBody('ok', '/test', method='GET')
        self.assertBody('ok', '/test', method='POST')
        self.assertStatus(405, '/test', method='PUT')

    def test_apply(self):
        def revdec(func):
            def wrapper(*a, **ka):
                return reversed(func(*a, **ka))
            return wrapper

        @py3web.route('/nodec')
        @py3web.route('/dec', apply=revdec)
        def test(): return '1', '2'
        self.assertBody('21', '/dec')
        self.assertBody('12', '/nodec')

    def test_apply_list(self):
        def revdec(func):
            def wrapper(*a, **ka):
                return reversed(func(*a, **ka))
            return wrapper
        def titledec(func):
            def wrapper(*a, **ka):
                return ''.join(func(*a, **ka)).title()
            return wrapper

        @py3web.route('/revtitle', apply=[revdec, titledec])
        @py3web.route('/titlerev', apply=[titledec, revdec])
        def test(): return 'a', 'b', 'c'
        self.assertBody('cbA', '/revtitle')
        self.assertBody('Cba', '/titlerev')

    def test_hooks(self):
        @py3web.route()
        def test():
            return py3web.request.environ.get('hooktest','nohooks')
        @py3web.hook('before_request')
        def hook():
            py3web.request.environ['hooktest'] = 'before'
        @py3web.hook('after_request')
        def hook():
            py3web.response.headers['X-Hook'] = 'after'
        self.assertBody('before', '/test')
        self.assertHeader('X-Hook', 'after', '/test')

    def test_template(self):
        @py3web.route(template='test {{a}} {{b}}')
        def test(): return dict(a=5, b=6)
        self.assertBody('test 5 6', '/test')

    def test_template_opts(self):
        @py3web.route(template=('test {{a}} {{b}}', {'b': 6}))
        def test(): return dict(a=5)
        self.assertBody('test 5 6', '/test')

    def test_name(self):
        @py3web.route(name='foo')
        def test(x=5): return 'ok'
        self.assertEquals('/test/6', py3web.url('foo', x=6))

    def test_callback(self):
        def test(x=5): return str(x)
        rv = py3web.route(callback=test)
        self.assertBody('5', '/test')
        self.assertBody('6', '/test/6')
        self.assertEqual(rv, test)




class TestDecorators(ServerTestBase):
    ''' Tests Decorators '''

    def test_view(self):
        """ WSGI: Test view-decorator (should override autojson) """
        @py3web.route('/tpl')
        @py3web.view('stpl_t2main')
        def test():
            return dict(content='1234')
        result = '+base+\n+main+\n!1234!\n+include+\n-main-\n+include+\n-base-\n'
        self.assertHeader('Content-Type', 'text/html; charset=UTF-8', '/tpl')
        self.assertBody(result, '/tpl')

    def test_view_error(self):
        """ WSGI: Test if view-decorator reacts on non-dict return values correctly."""
        @py3web.route('/tpl')
        @py3web.view('stpl_t2main')
        def test():
            return py3web.HTTPError(401, 'The cake is a lie!')
        self.assertInBody('The cake is a lie!', '/tpl')
        self.assertInBody('401 Unauthorized', '/tpl')
        self.assertStatus(401, '/tpl')

    def test_truncate_body(self):
        """ WSGI: Some HTTP status codes must not be used with a response-body """
        @py3web.route('/test/:code')
        def test(code):
            py3web.response.status = int(code)
            return 'Some body content'
        self.assertBody('Some body content', '/test/200')
        self.assertBody('', '/test/100')
        self.assertBody('', '/test/101')
        self.assertBody('', '/test/204')
        self.assertBody('', '/test/304')

    def test_routebuild(self):
        """ WSGI: Test route builder """
        def foo(): pass
        py3web.route('/a/:b/c', name='named')(foo)
        py3web.request.environ['SCRIPT_NAME'] = ''
        self.assertEqual('/a/xxx/c', py3web.url('named', b='xxx'))
        self.assertEqual('/a/xxx/c', py3web.app().get_url('named', b='xxx'))
        py3web.request.environ['SCRIPT_NAME'] = '/app'
        self.assertEqual('/app/a/xxx/c', py3web.url('named', b='xxx'))
        py3web.request.environ['SCRIPT_NAME'] = '/app/'
        self.assertEqual('/app/a/xxx/c', py3web.url('named', b='xxx'))
        py3web.request.environ['SCRIPT_NAME'] = 'app/'
        self.assertEqual('/app/a/xxx/c', py3web.url('named', b='xxx'))

    def test_autoroute(self):
        app = py3web.Bottle()
        def a(): pass
        def b(x): pass
        def c(x, y): pass
        def d(x, y=5): pass
        def e(x=5, y=6): pass
        self.assertEqual(['/a'],list(py3web.yieldroutes(a)))
        self.assertEqual(['/b/<x>'],list(py3web.yieldroutes(b)))
        self.assertEqual(['/c/<x>/<y>'],list(py3web.yieldroutes(c)))
        self.assertEqual(['/d/<x>','/d/<x>/<y>'],list(py3web.yieldroutes(d)))
        self.assertEqual(['/e','/e/<x>','/e/<x>/<y>'],list(py3web.yieldroutes(e)))



class TestAppShortcuts(ServerTestBase):
    def setUp(self):
        ServerTestBase.setUp(self)

    def assertWraps(self, test, other):
        self.assertEqual(test.__doc__, other.__doc__)

    def test_module_shortcuts(self):
        for name in '''route get post put delete error mount
                       hook install uninstall'''.split():
            short = getattr(py3web, name)
            original = getattr(py3web.app(), name)
            self.assertWraps(short, original)

    def test_module_shortcuts_with_different_name(self):
        self.assertWraps(py3web.url, py3web.app().get_url)





if __name__ == '__main__': #pragma: no cover
    unittest.main()
