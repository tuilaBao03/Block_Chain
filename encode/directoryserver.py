from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from typing import Union

class DirectoryServer(DatagramProtocol):
    def __init__(self):
        self.peers = set()

    def datagramReceived(self, datagram, addr):
        datagram = datagram.decode("utf-8")
        if datagram == "sẵn sàng":
            addresses = "\n".join([str(x) for x in self.peers])
            self.transport.write(addresses.encode("utf-8"), addr)
            self.peers.add(addr)
            print(f"Peer {addr} đã kết nối")
        elif datagram == "exit":
            self.peers.discard(addr)
            print(f"Peer {addr} ngắt kết nối")


if __name__ == '__main__':
    port = 9999
    print(f"Directory Server listening on port: {port}")
    reactor.listenUDP(port, DirectoryServer())
    reactor.run()