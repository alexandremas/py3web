# -*- coding: utf-8 -*-
import py3web
from tools import ServerTestBase

class TestBasicAuth(ServerTestBase):

    def test__header(self):
        @py3web.route('/')
        @py3web.auth_basic(lambda x, y: False)
        def test(): return {}
        self.assertStatus(401)
        self.assertHeader('Www-Authenticate', 'Basic realm="private"')
