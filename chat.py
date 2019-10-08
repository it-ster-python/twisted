from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class Chat(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        self.sendLine("What's your name?".encode("utf-8"))

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line.decode("utf-8"))
        else:
            self.handle_CHAT(line.decode("utf-8"))

    def handle_GETNAME(self, name):
        if name in self.users:
            self.sendLine("Name taken, please choose another.".encode("utf-8"))
            return
        self.sendLine("Welcome, {}".format(name).encode("utf-8"))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        message = "<{0}> {1}".format(self.name, message)
        for name, protocol in self.users.items():
            if protocol != self:
                protocol.sendLine(message.encode("utf-8"))

    def connectionLost(self, reason):
        print(reason)
        if self.name in self.users:
            del self.users[self.name]


class ChatFactory(Factory):

    def __init__(self):
        self.users = {}

    def buildProtocol(self, addr):
        return Chat(self.users)


if __name__ == "__main__":
    reactor.listenTCP(5000, ChatFactory())
    reactor.run()
