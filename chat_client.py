from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
import event
from threading import Thread
import time

MESSAGE = []

class ChatClient(Protocol):

    def __init__(self, name):
        self.name = name
        self.state = "OFFLINE"
        self.work = True
        event.Event(name="new_message", callback=self.send_message)


    def connectionMade(self):
            pass
            


    def lineReceived(self, data):
        if state == "ONLINE":
            print(line.decode("utf-8"))
        elif state == "OFFLINE":
            print(line.decode("utf-8"))
            self.sendLine("{}/n".format(self.name).encode("utf-8"))
            self.state = "ONLINE"


    def connectionLost(self, reason):
        pass


    def send_message(self):
        try:
            message = MESSAGE[0]
        except IndexError:
            print("Error")
        else:
            MESSAGE.remove(message)
            self.send_line("{}".format(message).encode("utf-8"))



class chatClientFactory(ClientFactory):

    def __init__(self, name):
        self.name = name


    def clientConnectionFailed(self, connector, reason):
        print('Connection failed. Reason:', reason)


    def clientConnectionLost(self, connector, reason):
        print(reason)
        print("Close.")
        reactor.stop()


    def buildProtocol(self, addr):
        self.connection = ChatClient(self.name)
        message = Message()
        worker = Thread(target=message, message.add_message, args=(MESSAGE,))
        worker.start()
        return self.connection



class Test():

    @event.Event.origin("rest")
    def work(self):
        print("I generate event")

class Message():
    @event.Event.origin("new_message", post=True)
    def add_message(self, message):
        for _ in range(20):
            time.sleep(2)
            message.append("Text")


if __name__ == '__main__':



    # def executor():
    #     print("Event occured")


    # ev = event.Event(name = "rest")
    # ev.register("rest", executor)

    # test = Test()
    # test.work()


   chat = chatClientFactory('sergey')
   #reactor.connectTCP('192.168.4.123', 5000, chat)
   reactor.connectTCP('127.0.0.1', 5000, chat)
   reactor.run()