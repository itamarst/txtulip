"""
An asyncio event loop on top of the Twisted reactor.
"""

from collections import namedtuple

from asyncio.unix_events import SelectorEventLoop
from asyncio.base_events import BaseEventLoop

from twisted.internet.abstract import FileDescriptor


class _Callable(namedtuple("_Callable", "f args")):
    """
    A callable and its args, packaged in a comparable object.
    """
    def __call__(self):
        pass#return self.f(*self.args)


class _GenericFileDescriptor(FileDescriptor):
    """
    Dispatch read/write events to given callbacks.
    """
    def __init__(self, reactor, fd, read_callback, write_callback):
        FileDescriptor.__init__(self, reactor)
        self._fd = fd
        self._read_callback = read_callback
        self._write_callback = write_callback

    def doRead(self):
        pass#self._read_callback()

    def doWrite(self):
        pass#self._write_callback()

    def fileno(self):
        return self._fd


_noop = _Callable(lambda: None, ())


class TwistedEventLoop(SelectorEventLoop):
    """
    Asyncio event loop wrapping Twisted's reactor.
    """
    def __init__(self, reactor):
        BaseEventLoop.__init__(self)
        self._reactor = reactor
        self._twisted_descriptors = {}

    def add_reader(self, fd, callback, *args):
        if fd in self._twisted_descriptors:
            reader = self._twisted_descriptors[fd]
            reader._read_callback = _Callable(callback, args)
        else:
            reader = _GenericFileDescriptor(self._reactor,
                                            fd, _Callable(callback, args), _noop)
            self._twisted_descriptors[fd] = reader
        self._reactor.addReader(reader)

    def add_writer(self, fd, callback, *args):
        if fd in self._twisted_descriptors:
            writer = self._twisted_descriptors[fd]
            writer._write_callback = _Callable(callback, args)
        else:
            writer = _GenericFileDescriptor(self._reactor,
                                            fd, _noop, _Callable(callback, args))
            self._twisted_descriptors[fd] = writer
        self._reactor.addWriter(writer)

    def remove_reader(self, fd):
        try:
            descriptor = self._twisted_descriptors.pop(fd)
        except KeyError:
            return
        self._reactor.removeReader(descriptor)

    def remove_writer(self, fd):
        try:
            descriptor = self._twisted_descriptors.pop(fd)
        except KeyError:
            return
        self._reactor.removeWriter(descriptor)
