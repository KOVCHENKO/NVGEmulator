from twisted.internet import reactor
import os
from NVGEmulator.TwistedReceiverProtocol import TwistedReceiverProtocolFactory


# il_kow: receiving packets through twisted
if __name__ =='__main__':
    print("Starting Server")
    factory = TwistedReceiverProtocolFactory()
    reactor.listenTCP(2999, factory)
    reactor.listenTCP(2998, factory)
    reactor.listenTCP(2997, factory)
    reactor.listenTCP(2996, factory)

    reactor.run()
else:
    print('IM A THREAD NUMBER: ' + str(os.getpid()))
