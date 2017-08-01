from multiprocessing import Process, Manager, SimpleQueue
import os


class ServerPool:
    _instance = None
    _manager = None
    server_pool = []

    @staticmethod
    def getInstance():
        if (ServerPool._instance == None):
            ServerPool._instance = ServerPool()
        return ServerPool._instance

    def doJob(list, nav_sender):
        print("Sending information")
        nav_sender.sendPacket()
        return

    def addProcess(self, nav_sender):
        for p in self.server_pool:
            if not p.is_alive():
                self.server_pool.remove(p)
        if len(self.server_pool) > 5:
            return
        p = Process(target=ServerPool.doJob, args=(self.server_pool, nav_sender))
        self.server_pool.append(p)
        p.start()
        return
