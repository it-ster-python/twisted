from twisted.internet.protocol import Protocol, ServerFactory
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

import random
import requests


URLS = [
    "http://rus-linux.net/MyLDP/BOOKS/Architecture-Open-Source-Applications/Vol-2/twisted-02.html",
    "http://qaru.site/questions/4510087/twisted-portforward-proxy-send-back-data-to-client",
    "https://html5.by/blog/run-http-server-from-current-directory/"
]


class Echo(Protocol):

    def __init__(self):
        super().__init__()
        data = requests.get(URLS[random.randint(0, 2)])
        print(dir(data))
        print(data.headers)
        lines = []
        for key, value in data.headers.items():
            lines.append(f"{key} {value}")
        header = "\r\n".join(lines + ["\r\n\r\n"])
        html = data.text
        self.response = f"{header}{html}".encode("utf-8")

    def dataReceived(self, data):
        self.transport.write(self.response)
        self.transport.loseConnection()


class SrvFactory(ServerFactory):

    def __init__(self, file_name):
        self.file = file_name

    def buildProtocol(self, addr):
        self.fd.write("{}\n".format(addr))
        return Echo()

    def startFactory(self):
        self.fd = open(self.file, "a")

    def stopFactory(self):
        self.fd.close()



if __name__ == '__main__':
    endpoint = TCP4ServerEndpoint(reactor, 5000)
    endpoint.listen(SrvFactory("server.log"))
    reactor.run()
