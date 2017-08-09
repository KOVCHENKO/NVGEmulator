from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.protocols.policies import TimeoutMixin


# il_kow: receiving packets through twisted
class TwistedReceiverProtocol(LineReceiver, TimeoutMixin):

    name = ""

    def getName(self):
        if self.name != "":
            return self.name
        return self.transport.getPeer().host

    def connectionMade(self):
        print("Connection has been made")
        self.setTimeout(30)

    def connectionLost(self, reason):
        print("Connection has been lost")

    def dataReceived(self, data):
        print("received data:", data[1:5])
        rdata = 'U'.encode() + data
        self.transport.write(rdata[0:5])

    def timeoutConnection(self):
        self.transport.abortConnection()


class TwistedReceiverProtocolFactory(ServerFactory):

    protocol = TwistedReceiverProtocol

    def __init__(self):
        self.clientProtocols = []
