from socket import*

class Client():
        rfcList #dictionary to store rfc files with their number, version, and title
        serverPort = 7734 #predefined port number for server
        serverName #should be predefined later
    def __init__(self, hostName, hostPort):
        self.hostName = hostName
        self.hostPort = hostPort
        self.clientSocket
    def connectServer(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((Client.serverName, Client.serverPort))
    def addMsg(self):
        msg = ''
        for rfc in rfcList:
            msg = msg + f'ADD RFC {rfc[0]} P2P-CI/{rfc[1]} \n Host: {self.hostName} \n Port: {self.hostPort} \n
                    Title: {rfc[2]} \n'
        return msg
    def lookupMsg(self):

    def listMsg(self):

    def sendStream(self):
        msg = self.addMsg()
        msg = raw_input(f'msg')
        self.clientSocketsend(msg)




