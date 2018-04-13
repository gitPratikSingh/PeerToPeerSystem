from socket import*
import threading
import os

class Server:
    clientList #each element is [host name, port number]
    rfcList  #[number, title, host]
    serverPort = 7734

    def __init__(self):
        self.serverSocket = self.listen()
        self.clientList = list()
        self.rfcList = list()

    def addRFCList(self, parse):
        clientList

    def removeRFCList(self):

    def listManage(self):

    def listen(self):
        server_socket = socket(AF_INET,SOCK_STREAM)
        server_socket.bind('',self.serverPort)
        server_socket.listen()
        print('The server is up!')
        return server_socket

    def OKconnect(self, connectionSocket):
        msg = 'P2P-CI/1.0 200 OK'
        self.sendStream(connectionSocket, msg)

    def BADREQUESTconnect(self, connecitonSocket):
        msg = 'P2P-CI/1.0 400 Bad Request'
        self.sendStream(connecitonSocket, msg)

    def sendStream(self, connectionSocket, msg):
        msg = raw_input(f'{msg}')
        connectionSocket.send(msg)

    def addOK(self, connectionSocket, request):
        rfcs = request.split('ADD')
        rfcs.pop(0)
        msg = 'P2P-CI/1.0 200 OK\n'
        host = ''
        for rfc in rfcs:
            lines = rfc.split('\n')
            lines[0] = lines[0][1:]
            for counter, line in enumerate(lines):
                if counter == 1:
                    host = words[1]
                if counter == 0:
                    words = line.split(' ')
                    msg += f'{words[0]} {words[1]} '
                else:
                    words = line.split(':')
                    msg += words[1]  #rfc number host port title
            msg += '\n'
        self.sendStream(connectionSocket, msg)
        return [msg, host]

    def addRFC(self,msg, host):
        lines = msg.split('\n')
        lines.pop(0)
        for line in lines:
            words = line.split(' ')
            self.rfcList.append([words[1], words[4], words[2]])

    def verNotSupport(self, connectionSocket):
        msg = 'P2P-CI/1.0 505 P2P-CI Version Not Supported'
        self.sendStream(connectionSocket, msg)

    def lookup(self, connectionSocket, request):
        

    def p2s_server(self):
        server1 = Server()
        while 1:
            connectionSocket, addr = server1.serverSocket.accept()
            request = connectionSocket.recv(1024)
            parse = request.split('\n')
            if parse[0] != 'REGISTER':
                server1.BADREQUESTconnect(connecitonSocket)
                connectionSocket.close()
                continue
            else:
                server1.OKconnect(connectionSocket)
                server1.clientList.append([parse[1], parse[2]])
                try:
                    thread_second = threading.Thread(target=self.server_client, args=(connectionSocket))
                    thread_second.daemon = True
                    thread_second.start()
                    thread_second.join()

                except KeyboardInterrupt:
                    sys.exit(0)

    def server_client(self, connectionSocket):
        request = connectionSocket.recv(1024)
        lines = request.split('\n')
        words = lines[0].split(' ')
        version = words[3].split('/')
        if float(version[1]) > 1.0
            self.verNotSupport(connectionSocket)
        elif words[0] == 'ADD':
            msgs = self.addOK(connectionSocket,request)
            self.addRFC(msgs[0], msgs[1])
        elif words[0] == 'LOOKUP'
            self.lookup(connectionSocket,request)
        elif words[0] == 'LIST'
            self.lisrOK(connectionSocket,request)

    if __main__ == "__main__":
        try:
            thread_first = threading.Thread(target=self.p2s_server)
            thread_first.daemon = True
            thread_first.start()
            thread_first.join()

        except KeyboardInterrupt:
            sys.exit(0)

