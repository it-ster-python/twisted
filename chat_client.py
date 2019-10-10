from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor
from twisted.protocols.basic import LineReceiver
import event

from threading import Thread
import time

MESSAGE = []

class Message():

    @event.Event.origin("new_message", post=True)
    def add_message(self, message):
        for _ in range(20):
            time.sleep(2)
            message.append("Text")

class ChatClient(LineReceiver):

    def __init__(self, name):
        self.name = name
        self.state = "OFFLINE"
        self.work = True
        event.Event(name="new_message", callback=self.send_message)

    def connectionMade(self):
        pass

    def lineReceived(self, line):
        if self.state == "ONLINE":
            print(line.decode("utf-8"))
        elif self.state == "OFFLINE":
            print(line.decode("utf-8"))
            self.sendLine("{}".format(self.name).encode("utf-8"))
            self.state = "ONLINE"

    def connectionLost(self, reason):
        print("Lost.")
        self.work = False

    def send_message(self, *args, **kwargs):
        try:
            message = MESSAGE[0]
        except IndexError:
            print("ERROR")
        else:
            del MESSAGE[0]
            self.sendLine("{}".format(message).encode("utf-8"))


class ChatClientFactory(ClientFactory):

    def __init__(self, name):
        self.name = name

    def clientConnectionFailed(self, connector, reason):
        print("Failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Close.")
        reactor.stop()

    def buildProtocol(self, addr):
        self.connection = ChatClient(self.name)
        message = Message()
        worker = Thread(target=message.add_message, args=(MESSAGE,))
        worker.start()
        return self.connection


if __name__ == "__main__":

    # TODO запилить парсер аргументов
    chat = ChatClientFactory("Vasia")
    reactor.connectTCP("127.0.0.1", 5000, chat)
    reactor.run()
