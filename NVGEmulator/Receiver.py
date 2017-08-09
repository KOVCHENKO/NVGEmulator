import socket


# il_kow: receiving packets through sockets
class Receiver:
    TCP_IP = '127.0.0.1'  # by default
    TCP_PORT = 1999  # by default
    BUFFER_SIZE = 1024

    def __init__(self, TCP_IP, TCP_PORT):
        self.TCP_IP = TCP_IP
        self.TCP_PORT = TCP_PORT

    def initialize(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.TCP_IP, self.TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        print('Connection address:', addr)
        while 1:
            data = conn.recv(self.BUFFER_SIZE)
            if not data: break
            rdata = 'U'.encode() + data
            print("received data:", data[1:5])
            conn.send(rdata[0:5])  # echo
        conn.close()


