Py3web Web Framework
====================

.. image:: http://py3webpy.org/docs/dev/_static/logo_nav.png
  :alt: Py3web Logo
  :align: right

Py3web aims to be a  modular framework for web applications.

The core features include offers request dispatching (URL routing) with URL parameter support, templates,
a built-in HTTP Server and adapters for many third party WSGI/HTTP-server and
template engines - all in a single file and with no dependencies other than the
Python Standard Library.

Additional features planned to be released as modules and are:

- authentication
- database interfaces
- form generation and validators


#TODO: Homepage and documentation: http://py3web.hipercenter.com/
License: MIT (see LICENSE)

Installation and Dependencies
-----------------------------

##TODO: Install py3web with ``pip install py3web`` or just `download at TODO and place it in your project directory. There are no (hard) dependencies other than the Python Standard Library.


Example
-------

.. code-block:: python

    from py3web import route, run

    @route('/hello/<name>')
    def hello(name):
        return '<h1>Hello %s!</h1>' % name.title()

    run(host='localhost', port=8080)
