from socket import*

class Client():
        rfcList #dictionary to store rfc files with their title, number, and version
    def __init__(self, hostName, hostPort, serverName):
        self.hostName = hostName
        self.hostPort = hostPort
        self.serverName = serverName
        self.serverPort = 7734 #predefined port number for server
        self.clientSocket
    def connectServer(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((self.serverName, self.serverPort))
        Client.addMsg(self)
    def addMsg(self):
        msg = 'ADD'

