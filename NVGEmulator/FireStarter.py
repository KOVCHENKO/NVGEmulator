from NVGEmulator.Receiver import Receiver
import asyncio

#  il_kow: receiving packets through sockets
@asyncio.coroutine
def starter(address, port):
    nvgEmu1 = Receiver(address, port)
    print("FIRST INITIALIZED + port: {0}".format(port))
    nvgEmu1.initialize()


print("Receiver has been started")
loop = asyncio.get_event_loop()
socks = [
    starter('127.0.0.1', 2999),
]

loop.run_until_complete(asyncio.wait(socks))
loop.close()
