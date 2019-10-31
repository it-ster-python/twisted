from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import json

class Chat(LineReceiver):

    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        data = {
        "status": "OK",
        "message": "what's your name?"
        }
        self.sendLine(json.dump(data).encode("utf-8"))
        

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_GETNAME(line.decode("utf-8"))
        else:
            self.handle_CHAT(line.decode("utf-8"))

    def handle_GETNAME(self, line):
        data = json.loads(line)
        print(data["login"], data["password"])
        if data["login"] in self.users:
            data= json.dumps(
                {
                "status": "ERROR", 
                "message": "Name taken, please choose another."
                }
                )
            self.sendLine(data.encode("utf-8"))
            return
        response = json.dumps(
            {
            "status": "OK", 
            "message": f"Welcome {data['login']}"
            }
        )
        self.sendLine(response.encode("utf-8"))
        self.name = data["login"]
        self.users[data["login"]] = self
        self.state = "CHAT"

    def handle_CHAT(self, message):
        data = json.dumps({"login": self.name, "message": message})
        #message = "<{0}> {1}".format(self.name, message)
        for name, protocol in self.users.items():
            if protocol != self:
                protocol.sendLine(data.encode("utf-8"))

    def connectionLost(self, reason):
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
