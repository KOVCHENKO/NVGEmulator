import socket

class Receiver:

    TCP_IP = '127.0.0.1'
    TCP_PORT = 2999
    BUFFER_SIZE = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))
    s.listen(1)

    conn, addr = s.accept()
    print('Connection address:', addr)
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        rdata = 'U'.encode() + data
        print("received data:", data[1:5])
        conn.send(rdata[0:5])  # echo
    conn.close()