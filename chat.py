from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
import json
from data import models


class Chat(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"

    def connectionMade(self):
        data = {"status": "OK", "message": "What's your name?"}
        self.sendLine(json.dumps(data).encode("utf-8"))

    def lineReceived(self, line):
        if self.state == "GETNAME":
            self.handle_AUTH(line.decode("utf-8"))
        else:
            self.handle_CHAT(line.decode("utf-8"))

    def handle_AUTH(self, line):
        data = json.loads(line)
        if data.get("login") in self.users:
            response = json.dumps(
                {
                    "status": "ERROR",
                    "message": "Name taken, please choose another",
                }
            )
            self.sendLine(response.encode("utf-8"))
            return
        try:
            user = models.User.get(login=data.get("login"))
        except models.User.DoesNotExist:
            response = json.dumps(
                {
                    "status": "ERROR",
                    "message": f"User {data.get('login')} not found.",
                }
            )
            self.sendLine(response.encode("utf-8"))
            return
        else:
            if user.check_password(data.get("password")):
                response = json.dumps(
                    {"status": "OK", "message": f"Welcome {data['login']}."}
                )
                self.sendLine(response.encode("utf-8"))
                self.name = data["login"]
                self.users[data["login"]] = self
                self.state = "CHAT"
            else:
                response = json.dumps(
                    {"status": "ERROR", "message": "Invalid password."}
                )
                self.sendLine(response.encode("utf-8"))

    def handle_CHAT(self, message):
        data = json.dumps({"login": self.name, "message": message})
        for name, protocol in self.users.items():
            if protocol != self:
                protocol.sendLine(data.encode("utf-8"))

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
