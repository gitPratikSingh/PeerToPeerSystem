from socket import*

class P2P_Client():
    rfcList #List of lists [[RFC#, RFC_TITLE]]


    serverPort = 7734 #predefined port number for server
    serverName #should be predefined later

    def __init__(self, hostName, hostPort):
        self.hostName = hostName
        self.hostPort = hostPort
        self.fetchLocalRFCs()
        self.connectServer()
        self.sendRFCList()

    def fecthLocalRFCs(self):
        # to be implemented
        # returns a list of the existing RFCs
        # read data directory and set rfcList


    def connectServer(self):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((Client.serverName, Client.serverPort))

    def sendRFCList(self):
        msg = ''
        for rfc in rfcList:
            msg = msg + self.ADD(rfc)
        return msg

    def sendStream(self, msg):
        msg = raw_input(f'msg')
        self.clientSocket.send(msg)

    def recvStream(self):
        return self.clientSocket.recv(1024)


    def ADD(self, rfc):
        # request
        msg = f'ADD RFC {rfc[0]} P2P-CI/1.0 \n Host: {self.hostName} \n Port: {self.hostPort} \n Title: {rfc[1]} \n'
        self.sendStream(msg)

        # response
        recvmsg = self.recvStream()
        print(recvmsg)


    def LIST(self):
        # request
        msg = f'LIST ALL P2P-CI/1.0 \n Host: {self.hostName} \n Port: {self.hostPort} \n'
        self.sendStream(msg)

        #response
        recvmsg = self.recvStream()
        print(recvmsg)

    def LOOKUP(self, rfc):
        # request
        msg = f'LOOKUP RFC {rfc[0]} P2P-CI/1.0 \n Host: {self.hostName} \n Port: {self.hostPort} \n Title: {rfc[1]} \n'
        self.sendStream(msg)

        # response
        recvmsg = self.recvStream()
        print(recvmsg)