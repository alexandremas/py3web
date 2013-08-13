#!/usr/bin/env python

import sys
import os
from distutils.core import setup

if sys.version_info < (3,3):
    raise NotImplementedError("Sorry, you need at least Python 3.3 to use py3web.")

import py3web

setup(name='py3web',
      version=py3web.__version__,
      description='Modular Pyhon 3.3+ WSGI-framework for web-applications.',
      long_description=py3web.__doc__,
      author=py3web.__author__,
      author_email='alexandre@hipercenter.com',
      url='http://py3web.hipercenter.com/',
      py_modules=['py3web'],
      scripts=['py3web.py'],
      license='MIT',
      platforms = 'any',
      classifiers=['Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 3.3',
        ],
     )



