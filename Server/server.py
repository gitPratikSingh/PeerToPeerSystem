from socket import*
import threading
import os

class RFCRecord:
    def __init__(self, rfc_number=-1, rfc_title='None', peerHostname='None', client_port=10000):
        self.rfc_number = rfc_number
        self.rfc_title = rfc_title
        self.peerHostname = peerHostname
        self.client_port = client_port

    def __str__(self):
        return f'{self.rfc_number} {self.rfc_title} {self.peerHostname}'

class clientRecord:
    def __init__(self, peerHostname='None', peerPortNo=10000):
        self.peerHostname = peerHostname
        self.peerPortNo = peerPortNo

    def __str__(self):
        return f'{self.peerHostname} {self.peerPortNo}'

class Server:
    clientList #each element is [host name, port number]
    rfcList  #[number, title, host]
    serverPort = 7734

    def __init__(self):
        self.serverSocket = self.listen()
        self.clientList = list()
        self.rfcList = list()

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
                    msg += words[1]
            msg += '\n' #each line format is: RFC {number} {host} {port} {title}
        self.sendStream(connectionSocket, msg)
        return [msg, host]

    def addRFC(self,msg, host):
        lines = msg.split('\n')
        lines.pop(0)
        for line in lines:
            words = line.split(' ')
            self.rfcList.insert(0, RFCRecord(words[1], words[4], words[2], words[3])) #[1]->number;[4]->title;[2]->host name;[3]->port

    def verNotSupport(self, connectionSocket):
        msg = 'P2P-CI/1.0 505 P2P-CI Version Not Supported'
        self.sendStream(connectionSocket, msg)

    def lookup(self, connectionSocket, request):
        lookup_list = list()
        lines = request.split('\n')
        port_line = lines[2].split(' ')
        port_num = port_line[1]
        code = -1
        flag = 0
        for rfc in rfcList:
            if int(rfc.rfc_number) == int(port_num)
                lookup_list.append(RFCRecord(rfc.rfc_number, rfc.rfc_title, rfc.peerHostname, rfc.client_port))
                flag = 1
                code = 200
        if flag == 0
            code = 404
        return code, lookup_list

    def listOK(self, connectionSocket, request):
        listall_list = list()
        for rfc in self.rfcList:
            listall_list.append(RFCRecord(rfc.rfc_number, rfc.rfc_title, rfc.peerHostname, rfc.client_port))
        return listall_list

    def clientLeave(self, connectionSocket, msg):
        lines = msg.split('\n')
        host_name = lines[1]
        for counter, client in enumerate(self.clientList):
            if client.peerHostname == host_name:
                self.clientList.pop(counter)
        for counter, rfc in enumerate(self.rfcList):
            if rfc.peerHostname == host_name:
                self.rfcList.pop(counter)

    def p2s_server(self):
        server1 = Server()
        while 1:
            connectionSocket, addr = server1.serverSocket.accept()
            request = connectionSocket.recv(1024)
            parse = request.split('\n')
            if parse[0] != 'REGISTER': #parse[0] = request type
                server1.BADREQUESTconnect(connecitonSocket)
                connectionSocket.close()
                continue
            else:
                server1.OKconnect(connectionSocket)
                server1.clientList.insert(0, clientRecord(parse[1], parse[2]) #parse[1]->host name and parse[2] -> port number
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
        words = lines[0].split(' ') #words->[type, RFC number, version]
        version = words[3].split('/')
        while 1:
            if float(version[1]) > 1.0
                self.verNotSupport(connectionSocket)
            elif words[0] == 'ADD':
                msgs = self.addOK(connectionSocket,request)
                self.addRFC(msgs[0], msgs[1]) #msgs[0]->response to add; msgs[1]->client name
            elif words[0] == 'LOOKUP':
                code, lookup_list = self.lookup(connectionSocket,request)
                if code == 200
                    msg = 'P2P-CI/1.0 200 OK\n'
                    for rfc in lookup_list:
                        msg += f'RFC {rfc.rfc_number} {rfc.rfc_title} {rfc.peerHostname} {rfc.client_port}\n'
                elif code == 404:
                    msg = 'P2P-CI/1.0 404 Not Found'
                self.sendStream(connectionSocket, msg)
            elif words[0] == 'LIST':
                msg = 'P2P-CI/1.0 200 OK\n'
                listall_list = self.listOK(connectionSocket,request)
                for rfc in listall_list:
                    msg += f'RFC {rfc.rfc_number} {rfc.rfc_title} {rfc.peerHostname} {rfc.client_port}\n'
                self.sendStream(connectionSocket, msg)
            elif words[0] == 'LEAVE':
                self.clientLeave(connectionSocket, msg)
                msg = 'P2P-CI/1.0 200 OK'
                self.sendStream(connectionSocket, msg)
                connectionSocket.close()
                return

    if __main__ == "__main__":
        try:
            thread_first = threading.Thread(target=self.p2s_server)
            thread_first.daemon = True
            thread_first.start()
            thread_first.join()

        except KeyboardInterrupt:
            sys.exit(0)

