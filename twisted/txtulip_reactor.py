"""
Twisted plugin providing the tulip/asyncio-based reactor.
"""

from twisted.application.reactors import Reactor

asyncio = Reactor('tulip', 'txtulip.reactor',
                  'A reactor based on the tulip/asyncio library.')
