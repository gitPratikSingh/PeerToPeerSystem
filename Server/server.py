import socket
import threading
import os
import sys


class RFCRecord:
    def __init__(self, rfc_number=-1, rfc_title='None', clientName='None', client_port=10000):
        self.rfc_number = rfc_number
        self.rfc_title = rfc_title
        self.clientName = clientName
        self.client_port = client_port

    def __str__(self):
        return f'{self.rfc_number} {self.rfc_title} {self.clientName}'


class clientRecord:
    def __init__(self, clientName='None', client_port=10000):
        self.clientName = clientName
        self.client_port = client_port

    def __str__(self):
        return f'{self.clientName} {self.client_port}'


class Server:
    clientList = list()
    rfcList = list()
    serverPort = 7734
    serverName = 'localhost'

    def __init__(self):
        self.serverSocket = self.listen()

    def listen(self):
        server_socket = socket.socket()
        server_socket.bind((self.serverName, self.serverPort))
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
            msg_host = ''
            title = ''
            port = ''
            for counter, line in enumerate(lines):

                if counter == 0:
                    words = line.split(' ')
                    msg += f'{words[0]} {words[1]} '
                elif counter == 1:
                    words = line.split(':')
                    host = words[1][1:]
                    msg_host = words[1]
                elif counter == 2:
                    words = line.split(':')
                    port = words[1]
                elif counter == 3:
                    words = line.split(':')
                    title = words[1]
            msg += f'{title}{msg_host}{port}\n'     #each line format is: RFC {number} {host} {port} {title}
        self.sendStream(connectionSocket, msg)
        return msg, host

    def addRFC(self, msg):
        lines = msg.split('\n')
        lines.pop(0)
        for line in lines:
            words = line.split(' ')
            Server.rfcList.insert(0, RFCRecord(words[1], words[2], words[3], words[4])) #number,title,host name,port

    def verNotSupport(self, connectionSocket):
        msg = 'P2P-CI/1.0 505 P2P-CI Version Not Supported'
        self.sendStream(connectionSocket, msg)

    def lookup(self, request):
        lookup_list = list()
        lines = request.split('\n')
        rfc_line = lines[0].split(' ')
        rfc_num = rfc_line[2]
        response_code = -1
        flag = 0
        for rfc in Server.rfcList:
            if int(rfc.rfc_number) == int(rfc_num):
                lookup_list.append(RFCRecord(rfc.rfc_number, rfc.rfc_title, rfc.clientName, rfc.client_port))
                flag = 1
                response_code = 200
        if flag == 0:
            response_code = 404
        return response_code, lookup_list

    def listOK(self):
        listall_list = list()
        for rfc in Server.rfcList:
            listall_list.append(RFCRecord(rfc.rfc_number, rfc.rfc_title, rfc.clientName, rfc.client_port))
        return listall_list

    def clientLeave(self, msg):
        lines = msg.split('\n')
        host_name = lines[1]
        for counter, client in enumerate(Server.clientList):
            if client.clientName == host_name:
                Server.clientList.pop(counter)
        for counter, rfc in enumerate(Server.rfcList):
            if rfc.clientName == host_name:
                Server.rfcList.pop(counter)


def p2s_server():
    server1 = Server()
    while 1:
        connectionSocket, addr = server1.serverSocket.accept()
        request = connectionSocket.recv(1024)
        parse = request.split('\n')
        if parse[0] != 'REGISTER': # parse[0] = request type
            server1.BADREQUESTconnect(connecitonSocket)
            connectionSocket.close()
            continue
        else:
            server1.OKconnect(connectionSocket)
            Server.clientList.insert(0, clientRecord(parse[1], parse[2])) #parse[1]->host name and parse[2] -> port number
            try:
                thread_second = threading.Thread(target=server_client, args=(server1, connectionSocket))
                thread_second.daemon = True
                thread_second.start()
                thread_second.join()

            except KeyboardInterrupt:
                sys.exit(0)


def server_client(self, connectionSocket):
    request = connectionSocket.recv(1024)
    lines = request.split('\n')
    words = lines[0].split(' ')  # words->[type, RFC number, version]
    version = words[3].split('/')
    while 1:
        if float(version[1]) > 1.0:
            self.verNotSupport(connectionSocket)
        elif words[0] == 'ADD':
            msg = self.addOK(connectionSocket,request)
            self.addRFC(msg)  # msg->response to add
        elif words[0] == 'LOOKUP':
            code, lookup_list = self.lookup(request)
            msg = ''
            if code == 200:
                msg = 'P2P-CI/1.0 200 OK\n'
                for rfc in lookup_list:
                    msg += f'RFC {rfc.rfc_number} {rfc.rfc_title} {rfc.clientName} {rfc.client_port}\n'
            elif code == 404:
                msg = 'P2P-CI/1.0 404 Not Found'
            self.sendStream(connectionSocket, msg)
        elif words[0] == 'LIST':
            msg = 'P2P-CI/1.0 200 OK\n'
            listall_list = self.listOK()
            for rfc in listall_list:
                msg += f'RFC {rfc.rfc_number} {rfc.rfc_title} {rfc.clientName} {rfc.client_port}\n'
            self.sendStream(connectionSocket, msg)
        elif words[0] == 'REMOVE':
            self.clientLeave(request)
            msg = 'P2P-CI/1.0 200 OK'
            self.sendStream(connectionSocket, msg)
            connectionSocket.close()
            return


if __name__ == "__main__":
    try:
        thread_first = threading.Thread(target=p2s_server)
        thread_first.daemon = True
        thread_first.start()
        thread_first.join()

    except KeyboardInterrupt:
        sys.exit(0)

