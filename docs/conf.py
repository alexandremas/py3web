# -*- coding: utf-8 -*-

import sys, os, time

bottle_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'../'))
sys.path.insert(0, bottle_dir)
import py3web

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.viewcode']
master_doc = 'index'
project = u'Bottle'
copyright = unicode('2009-%s, %s' % (time.strftime('%Y'), py3web.__author__))
version = ".".join(py3web.__version__.split(".")[:2])
release = py3web.__version__
add_function_parentheses = True
add_module_names = False
pygments_style = 'sphinx'
intersphinx_mapping = {'python': ('http://docs.python.org/', None),
                       'werkzeug': ('http://werkzeug.pocoo.org/docs/', None)}

autodoc_member_order = 'bysource'

