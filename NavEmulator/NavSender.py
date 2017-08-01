from __future__ import print_function
from twisted.internet import reactor, protocol
from NavEmulator.ServerPool import ServerPool
import time


class EchoClient(protocol.Protocol):

    device_imei = '100000000000004'
    iterations_number = 20

    start_time = time.time()
    initial_iteration = 0

    # Here is the message which should be sent
    def connectionMade(self):
        first_message = "@NTC\x01\x00\x00\x00\x00\x00\x00\x00\x13\x00HC*>S:" + self.device_imei
        self.transport.write(first_message.encode())

    def dataReceived(self, data):
        print("Server said: ", data)
        if self.iterations_number == self.initial_iteration:
            self.transport.loseConnection()
            print("SENDER EXECUTION TIME: {}".format(time.time() - self.start_time))
        else:
            if data == b'@NTC\x00\x00\x00\x00\x01\x00\x00\x00\x03\x00E^*<S':  # Ответ на первое сообщение
                self.sendSecondMessage()
            elif data == b'@NTC\x00\x00\x00\x00\x01\x00\x00\x00\t\x00\xb1\xa0*<FLEX\xb0\x14\x14':  # Ответ на второе сообщение
                self.sendPacket()
            elif data == b'~T\x03\x00\x00\x00\x85':  # Ответ на отосланный пакет (отослать еще 10 таких же пакетов данных)
                # Отправка пакетов по потокам
                # server_pool = ServerPool()
                # server_pool.getInstance()
                # server_pool.addProcess(self)
                self.sendPacket()
                self.initial_iteration += 1
                print("INITIAL_ITERATIONS_COUNT: {}".format(self.initial_iteration))
            else:
                self.transport.loseConnection()



    def connectionLost(self, reason):
        print("Connection Lost")

    # Второе сообщение - проверка протокола
    def sendSecondMessage(self):
        self.transport.write(b'@NTC\x01\x00\x00\x00\x00\x00\x00\x00\x1a\x00\xec\xee*>FLEX\xb0\x14\x14z\xfb\xee0\x08\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    # Третье сообщение - отсылка пакета
    def sendPacket(self):
        self.transport.write(b'~T\x03\x00\x00\x00\x03\x00\x00\x00\x00\x10\xfa(\x7fY\x00\x00c\x01\xfa(\x7fY0\xc4U\x01\xf0\xa8\xfb\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xb7')


class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()

# connection to a server running on port 9055
def main():
    f = EchoFactory()
    reactor.connectTCP("localhost", 9000, f)
    reactor.run()