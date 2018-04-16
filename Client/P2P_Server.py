import socket
import threading
import re
import os
import platform
import datetime


class P2P_Server():

    def __init__(self, hostName, hostip, uploadPort):
        self.hostname = hostName
        self.hostip = hostip
        self.uploadPort = uploadPort

    def p2p_server_start(self):

        client_socket = socket.socket()
        client_socket.bind((self.hostip, self.uploadPort))
        client_socket.listen(2)

        print("Started listening for" + str(client_socket))
        while (1):
            (peer_socket, peer_addr) = client_socket.accept()
            #print("Connected to" + str(peer_addr))

            thread = threading.Thread(target=self.sendRFC, args=("sendRFC", peer_socket,))
            thread.start()
            thread.join()

        client_socket.close()
        return

    def sendStream(self, connectionSocket, msg):
        msg = msg.encode('utf-8')
        connectionSocket.send(msg)

    def sendRFC(self, name, sock):

        try:
            request = sock.recv(1024)
            request = request.decode('utf-8')

            lines = request.split('\n')
            words = lines[0].split(' ')  # words->[type, RFC, RFC number, version]
            regex = r"P2P-CI\/\d*.\d*"
            # print("msg:" +lines[0])
            match = re.search(regex, lines[0])
            first = match.group(0)
            version = first.split('/')

            if float(version[1]) > 1.0:
                msg = 'P2P-CI/1.0 505 P2P-CI Version Not Supported'
                self.sendStream(sock, msg)
            elif words[0] != 'GET':
                msg = 'P2P-CI/1.0 505 P2P-CI Operation Not Supported'
                self.sendStream(sock, msg)
            else:
                rfcSet = set()
                dataDir = os.path.join(os.getcwd(), 'RFC_REPO')
                file_list = os.listdir(dataDir)
                matchfile = ''
                for tmpfile in file_list:
                    rfc = tmpfile.split('.')[0].split('-')[1:3]
                    rfcSet.add(rfc[0])
                    if words[2] == rfc[0]:
                        matchfile = tmpfile

                if words[2] not in rfcSet:
                    print("File not found")
                    msg = 'P2P-CI/1.0 404 P2P-CI FILE NOT FOUND\n'
                    self.sendStream(sock, msg)

                else:
                    msg = "P2P-CI/1.0 200 OK" + "\n"
                    self.sendStream(sock, msg)
                    file_name = os.path.join(dataDir, matchfile)
                    msg = "Date: " +datetime.datetime.strftime(datetime.datetime.utcnow(),"%a, %d %b %Y %H:%M:%S %ZGMT\n")
                    msg = msg + "OS: %s" % platform.system() + ' ' + platform.release()+ "\n"
                    msg = msg + "Last-Modified: %s" % datetime.datetime.fromtimestamp(os.path.getmtime(file_name)).strftime("%a, %d %b %Y %H:%M:%S %ZGMT\n")
                    msg = msg + "Content-Length: %s" % os.path.getsize(file_name)

                    self.sendStream(sock, msg)

                    with open(file_name, 'r') as f:
                        msg = f.read(1024)
                        self.sendStream(sock, msg)
                        while msg != "":
                            msg = f.read(1024)
                            self.sendStream(sock, msg)
                        f.close()
        finally:
            sock.close()


if __name__ == "__main__":
    hostName = 'localhost'
    hostip = '127.0.0.1'
    uploadPort = 10001
    p2p_Server = P2P_Server(hostName, hostip, uploadPort)
    p2p_Server.p2p_server_start()
