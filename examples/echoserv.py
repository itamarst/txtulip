#!/usr/bin/env python3

# Install the tulip/asyncio reactor:
from txtulip.reactor import install
install()

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor


class Echo(Protocol):
    def dataReceived(self, data):
        self.transport.write(data)



def main():
    reactor.listenTCP(8000, Factory.forProtocol(Echo))
    reactor.run()



if __name__ == '__main__':
    main()
