txtulip: Twisted reactor based on Tulip/Asyncio/Trollius
========================================================

Twisted is a production-quality event-driven networking engine with built-in support for many protocols (HTTP, DNS, SSH, IMAP), and a large ecosystem of 3rd party libraries.
Twisted works on both Python 2 and a subset of functionality is supported on Python 3.

Asyncio (also known as Tulip) is a new networking event loop implementation included with Python 3.4, whose core networking layer was modeled on Twisted APIs.
Trollius is a backport of Asyncio to Python 2.

``txtulip`` aims to allow using both Twisted and Tulip/Asyncio/Trollius in the same Python process by:

1. Running the Twisted reactor on top of Asyncio's event loop.
2. Alternatively, running the Asyncio event loop on top of Twisted's reactor (work in progress).
3. Hooking up Deferreds and Futures (planned, no code yet).

``txtulip`` is licensed under the MIT open source license, and maintained by Itamar Turner-Trauring.

``txtulip`` can be downloaded at https://pypi.python.org/pypi/txtulip

Bugs and feature requests shoudl be filed at https://github.com/itamarst/txtulip


Status
^^^^^^

This package is experimental; pull requests are welcome.

Twisted on Asyncio
~~~~~~~~~~~~~~~~~~
The vast majority of the Twisted test suite does pass on the new reactor.
The remaining test failures are due to:

* Fragile or buggy tests in Twisted's test suite.
* Bugs in asyncio that do not exist in Twisted, especially in the epoll event loop (lack of support for large values in ``call_later``, lack of support for filesystem files which can happen e.g. when they are hooked up to stdin/out).
* Potentially, bugs in ``txtulip``.



Requirements
^^^^^^^^^^^^

* POSIX platform
* Either: Python 3.4, Twisted 14.0 and trunk
* Or: Python 2.7, Trollius, and a modern version of Twisted


Usage
^^^^^

Twisted on Asyncio
~~~~~~~~~~~~~~~~~~
Using txtulip is easy.
Before importing any Twisted code, install the ``txtulip`` reactor::

    from txtulip.reactor import install
    install()

See ``examples/echoserv.py`` for an example.

On Python 2 (or once trial/twistd command line tools are ported to Python 3), you can also specify ``trial --reactor=tulip`` or ``twistd --reactor=tulip``.

