txtulip: Twisted reactor based on Tulip/Asyncio/Trollius
========================================================

Twisted is a production-quality event-driven networking engine with built-in support for many protocols (HTTP, DNS, SSH, IMAP), and a large ecosystem of 3rd party libraries.
Twisted works on both Python 2 and a subset of functionality is supported on Python 3.

Asyncio (also known as Tulip) is a new networking event loop implementation included with Python 3.4, whose core networking layer was modeled on Twisted APIs.
Trollius is a backport of Asyncio to Python 2.

``txtulip`` lets you integrate both in the same Python 3 process by running the Twisted reactor on top of Asyncio's event loop.
An alternative (and arguably superior) solution would be to run the Asyncio event loop on top of Twisted's reactor, but that is not available yet.

``txtulip`` is licensed under the MIT open source license, and maintained by Itamar Turner-Trauring.

``txtulip`` can be downloaded at https://pypi.python.org/pypi/txtulip

Bugs and feature requests shoudl be filed at https://github.com/itamarst/txtulip


Requirements
^^^^^^^^^^^^

* POSIX platform
* Either: Python 3.4, Twisted 14.0 and trunk
* Or: Python 2.7, Trollius, and a modern version of Twisted


Usage
^^^^^

Using txtulip is easy.
Before importing any Twisted code, install the ``txtulip`` reactor::

    from txtulip.reactor import install
    install()

See ``examples/echoserv.py`` for an example.


News
^^^^

Release 0.1
~~~~~~~~~~~
* The vast majority of the Twisted test suite passes on the new reactor, except
  for a few edge cases that are the result of bugs in the test suite or
  unimportant differences.
