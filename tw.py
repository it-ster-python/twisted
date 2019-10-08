from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

import requests
import random

urls = [
'https://github.com/it-ster-python/network',
'http://rus-linux.net/',
'https://www.facebook.com/'
]

class Echo(Protocol):

    def __init__(self):
        super().__init__()
        data = requests.get(urls[random.randint(0,2)])
        lines = []
        for key, value in data.headers.items():
            lines.append(f"{key} {value}")
        header = "\r\n".join(lines+["/r/n/r/n"])
        html = data.text
        self.response = f"{header}{html}".encode("utf-8")

    def dataReceived(self, data):
        self.transport.write(self.response)
        self.transport.loseConnection()


class SrvFactory(ServerFactory):
    #protocol = Echo
    def __init__(self, file_name):
        self.file = file_name

    def buildProtocol(self, addr):
        print(addr)
        self.fd.write("{}/n".format(addr))
        return Echo()

    def startFactory(self):
        self.fd = open(self.file, "a")

    def stopFactory(self):
        print("stop")
        self.fd.close()

if __name__ == "__main__":
    #factory = SrvFactory()
    #reactor.listenTCP(5000, factory)
    #reactor.run()
    endpoint = TCP4ServerEndpoint(reactor, 5000)
    endpoint.listen(SrvFactory("server.log"))
    reactor.run()





#192.168.4.123