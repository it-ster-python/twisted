from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver

from threading import Thread
import time

MESSAGE = []

def sender(connection, storage):
    while True:
        print("sender")
        if len(storage):
            if storage != "close":
                connection.sendLine(storage[0].encode("utf-8"))
                storage = []
            else:
                connection.connectionLost()
                break
        else:
            time.sleep(1)



class ChatClient(LineReceiver):

    def __init__(self, name):
        self.name = name
        self.state = "OFFLINE"
        self.work = True

    def connectionMade(self):
        # worker = Thread(target=sender, args=(self,MESSAGE))
        # worker.start()
        pass

    def lineReceived(self, line):
        if self.state == "ONLINE":
            print(line.decode("utf-8"))
            worker = Thread(target=sender, args=(self,MESSAGE))
            worker.start()
        elif self.state == "OFFLINE":
            print(line.decode("utf-8"))
            self.sendLine("{}".format(self.name).encode("utf-8"))
            self.state = "ONLINE"

    def connectionLost(self, reason):
        print("Lost.")
        self.work = False

    def send_message(self, message):
        self.sendLine("{}".format(message).encode("utf-8"))


class ChatClientFactory(ClientFactory):

    def __init__(self, name):
        self.name = name
        self.message = "None"

    def clientConnectionFailed(self, connector, reason):
        print("Failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Close.")
        reactor.stop()

    def buildProtocol(self, addr):
        self.connection = ChatClient(self.name)
        return self.connection


if __name__ == "__main__":
    # import time

    # TODO запилить парсер аргументов
    chat = ChatClientFactory("Dima")
    reactor.connectTCP("192.168.4.123", 5000, chat)
    reactor.run()
    while True:
        MESSAGE.append("Message")
        time.sleep(3)
