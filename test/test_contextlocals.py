# -*- coding: utf-8 -*-
'''
Some objects are context-local, meaning that they have different values depending on the context they are accessed from. A context is currently defined as a thread.
'''

import unittest
import py3web
import threading


def run_thread(func):
    t = threading.Thread(target=func)
    t.start()
    t.join()

class TestThreadLocals(unittest.TestCase):
    def test_request(self):
        e1 = {'PATH_INFO': '/t1'}
        e2 = {'PATH_INFO': '/t2'}

        def run():
            py3web.request.bind(e2)
            self.assertEqual(py3web.request.path, '/t2')

        py3web.request.bind(e1)
        self.assertEqual(py3web.request.path, '/t1')
        run_thread(run)
        self.assertEqual(py3web.request.path, '/t1')

    def test_response(self):

        def run():
            py3web.response.bind()
            py3web.response.content_type='test/thread'
            self.assertEqual(py3web.response.headers['Content-Type'], 'test/thread')

        py3web.response.bind()
        py3web.response.content_type='test/main'
        self.assertEqual(py3web.response.headers['Content-Type'], 'test/main')
        run_thread(run)
        self.assertEqual(py3web.response.headers['Content-Type'], 'test/main')


if __name__ == '__main__': #pragma: no cover
    unittest.main()
