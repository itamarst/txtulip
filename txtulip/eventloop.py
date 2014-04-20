"""
An asyncio event loop on top of the Twisted reactor.
"""

from collections import namedtuple

from asyncio.unix_events import SelectorEventLoop
from asyncio.base_events import BaseEventLoop
from asyncio.events import TimerHandle
from asyncio import tasks

from twisted.internet.abstract import FileDescriptor


class _Callable(namedtuple("_Callable", "f args")):
    """
    A callable and its args, packaged in a comparable object.
    """
    def __call__(self):
        return self.f(*self.args)


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
        self._read_callback()

    def doWrite(self):
        self._write_callback()

    def fileno(self):
        return self._fd


_noop = _Callable(lambda: None, ())


# XXX sketch, reimplement TDD
class TwistedTimerHandle(TimerHandle):
    """TimerHandle for TwistedEventLoop."""
    __slots__ = ['_delayedcall']

    def __init__(self, delayedcall, when, callback, args, loop):
        super().__init__(when, callback, args, loop)
        self._delayedcall = delayedcall

    def cancel(self):
        super().cancel()
        self._delayedcall.cancel()


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
        if descriptor._write_callback is not _noop:
            descriptor._read_callback = _noop
            self._twisted_descriptors[fd] = descriptor

    def remove_writer(self, fd):
        try:
            descriptor = self._twisted_descriptors.pop(fd)
        except KeyError:
            return
        self._reactor.removeWriter(descriptor)
        if descriptor._read_callback is not _noop:
            descriptor._write_callback = _noop
            self._twisted_descriptors[fd] = descriptor


    # XXX sketch, disable and re-enable with TDD, unless it turns out
    # asyncio's test suite is sufficient.
    def run_forever(self):
        self._reactor.run()

    def stop(self):
        self._reactor.crash()

    def close(self):
        # XXX probably need to run reactor a bit more for real cleanup...
        self._reactor.stop()

    def is_running(self):
        return self._reactor.running

    def call_later(self, delay, callback, *args):
        return TwistedTimerHandle(
            self._reactor.callLater(delay, callback, *args),
            self.time() + delay, callback, args, self)

    def call_at(self, when, callback, *args):
        return self.callLater(when - self.time(), callback, *args)

    def time(self):
        return self._reactor.seconds()

    def call_soon_threadsafe(self, callback, *args):
        # XXX return a Handle
        self._reactor.callFromThread(callback, *args)

    def add_signal_handler(self, sig, callback, *args):
        raise NotImplementedError

    def remove_signal_handler(self, sig):
        raise NotImplementedError

    def run_until_complete(self, future):
        # XXX copied from Python, note license or write new version
        future = tasks.async(future, loop=self)
        future.add_done_callback(self.stop)
        self.run_forever()
        future.remove_done_callback(self.stsop)
        if not future.done():
            raise RuntimeError('Event loop stopped before Future completed.')

        return future.result()
