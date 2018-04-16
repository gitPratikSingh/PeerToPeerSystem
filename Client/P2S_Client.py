import socket
import threading
import os
import re
import sys
import P2P_Server


class P2P_Client():
    rfcList = list()  # List of lists [[RFC#, RFC_TITLE]]
    serverPort = 7734  # predefined port number for server
    serverName = 'localhost'  # should be predefined later

    def __init__(self, hostName, hostip, uploadPort):
        self.hostName = hostName
        self.uploadPort = uploadPort
        self.hostPort = uploadPort
        self.hostIP = hostip
        self.fetchLocalRFCs()
        self.connectServer()
        self.sendRegisterMessage()
        self.sendRFCList()
        self.p2p_server = P2P_Server.P2P_Server(hostName, hostip, uploadPort)
        print("P2S Init Successful")

    def fetchLocalRFCs(self):
        #populate the list of local RFCs
        dataDir = os.path.join(os.getcwd(), 'RFC_REPO')
        file_list = os.listdir(dataDir)
        for tmpfile in file_list:
            try:
                rfc = tmpfile.split('.')[0].split('-')[1:3]
                P2P_Client.rfcList.append(rfc)
            except IndexError:
                print(str(tmpfile) + " is not correct format")

    def sendRegisterMessage(self):
        # request
        msg = f'REGISTER P2P-CI/1.0 \nHost: {self.hostName} \nPort: {self.uploadPort} \n'
        self.sendStream(msg)

        # response
        recvmsg = self.recvStream()
        print(recvmsg)

    def connectServer(self):
        global serverName
        global serverPort
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.clientSocket)
        self.clientSocket.connect((P2P_Client.serverName, P2P_Client.serverPort))

    def sendRFCList(self):
        for rfc in P2P_Client.rfcList:
            self.ADD(rfc)

    def sendStream(self, msg, peerSocket=None):
        print(msg)
        if(peerSocket):
            peerSocket.send(msg.encode('utf-8'))
        else:
            self.clientSocket.send(msg.encode('utf-8'))

    def recvStream(self, peerSocket=None):
        if(peerSocket):
            msg = peerSocket.recv(1024)
        else:
            msg = self.clientSocket.recv(1024)
        return msg.decode('utf-8')

    def ADD(self, rfc):
        # request
        try:
            msg = f'ADD RFC {rfc[0]} P2P-CI/1.0\nHost: {self.hostName}\nPort: {self.hostPort}\nTitle: {rfc[1]}\n'
            self.sendStream(msg)
        except IndexError:
            print('RFC format not correct')
            return

        # response
        recvmsg = self.recvStream()
        print(recvmsg)

    def LIST(self):
        # request
        msg = f'LIST ALL P2P-CI/1.0\nHost: {self.hostName}\nPort: {self.hostPort}\n'
        self.sendStream(msg)

        # response
        recvmsg = self.recvStream()
        print(recvmsg)

    def LOOKUP(self, rfc):
        # request
        msg = f'LOOKUP RFC {rfc[0]} P2P-CI/1.0\nHost: {self.hostName}\nPort: {self.hostPort}\nTitle: {rfc[1]}\n'
        self.sendStream(msg)

        # response
        recvmsg = self.recvStream()
        print(recvmsg)

    def GET_RFC(self, rfc_number, rfc_title, peer_host_name, port_peer):
        peer_socket = socket.socket()
        peer_socket.connect((peer_host_name, port_peer))
        print("P2S connected")

        message = "GET RFC" + " " + str(
            rfc_number) + " " + "P2P-CI/1.0" + "\n" + "Host: " + peer_host_name + "\n" + "OS: Windows \n"
        file_name = 'rfc' + str(rfc_number) + "-" + 'rfc_title' + ".txt"

        self.sendStream(message, peerSocket=peer_socket)
        reply = self.recvStream(peerSocket=peer_socket)

        reply_list = reply.split(' ')
        dataDir = os.path.join(os.getcwd(), 'RFC_REPO')
        file_name = os.path.join(dataDir, file_name)

        if str(reply_list[1]) == '200':
            # todo, use content length and terminate the receive request accordingly
            recv_rfc_data = self.recvStream(peerSocket=peer_socket)
            regex = r"Content-Length: \d*"
            match = re.search(regex, recv_rfc_data)
            first = match.group(0)
            contentlength = (int)(first.split(': ')[1])

            rfc_file = open(file_name, 'wb')
            while contentlength>0:
                recv_rfc_data = peer_socket.recv(1024)
                if recv_rfc_data:
                    rfc_file.write(recv_rfc_data)
                    #print("Data writing" + str(contentlength))
                    contentlength = contentlength - len(recv_rfc_data)
                else:
                    rfc_file.close()

        else:
            print("File Not Found")

        peer_socket.close()

    def REMOVE_CLIENT(self):
        msg = "REMOVE P2P-CI/1.0 Host: " + self.hostName + "\n"
        self.sendStream(msg)
        # response
        recvmsg = self.recvStream()
        print(recvmsg)
        self.clientSocket.close()


def menu(p2p_client):
    while (1):
        print("Select from the List")
        print("1. List all RFC")
        print("2. Lookup RFC")
        print("3. Add RFC")
        print("4. Get RFC file")
        print("5. Exit")

        choice = int(input())

        if choice == 1:
            p2p_client.LIST()

        if choice == 2:
            print("Enter RFC number")
            rfc_number = int(input())
            print("Enter RFC title")
            rfc_title = input()

            rfc = list()
            rfc.append(rfc_number)
            rfc.append(rfc_title)

            p2p_client.LOOKUP(rfc)

        if choice == 3:
            print("Enter RFC number")
            rfc_number = input()
            print("Enter the title for the RFC")
            rfc_title = input()

            rfc = list()
            rfc.append(rfc_number)
            rfc.append(rfc_title)

            p2p_client.ADD(rfc)

        if choice == 4:
            print("Enter RFC number")
            rfc_number = input()
            try:
                rfc_number = (int)(rfc_number)
            except ValueError:
                if rfc_number != '':
                    print("Please enter an integer for rfc")
                    return

            print("Enter the title for the RFC")
            rfc_title = input()
            print("Enter Peer's Hostname")
            peer_host_name = input()
            print("Enter Peer port number")
            port_peer = input()
            try:
                port_peer = (int)(port_peer)
            except ValueError:
                if port_peer!='':
                    print("Please enter an integer for port_peer")
                    return

            rfc_number = 2822 if rfc_number == '' else rfc_number
            rfc_title= 'Internet Message Format' if rfc_title == '' else rfc_title
            peer_host_name='localhost' if peer_host_name == '' else peer_host_name
            port_peer = 12345 if port_peer == '' else port_peer
            p2p_client.GET_RFC(rfc_number, rfc_title, peer_host_name, port_peer)

        if choice == 5:
            p2p_client.REMOVE_CLIENT()
            print("bye!")


def main():
    print("Enter IP address of the host (Enter for default value)")
    IP = input()
    print("Enter Host name (Enter for default value)")
    HOST = input()
    print("Enter Upload Port number (Enter for default value)")
    PORT = input()
    try:
        PORT = (int)(PORT)
    except ValueError:
        if PORT !='':
            print("Please enter an integer for port")
            return

    #[on_true] if [expression] else [on_false]

    IP = '127.0.0.1' if IP == '' else IP
    HOST = 'localhost' if HOST == '' else HOST
    PORT = 12345 if PORT == '' else PORT
    p2p_client = P2P_Client(HOST, IP, PORT)

    try:
        print("In main")
        thread_first = threading.Thread(target=p2p_client.p2p_server.p2p_server_start)
        thread_second = threading.Thread(target=menu, args=(p2p_client,))
        thread_first.daemon = True
        thread_second.daemon = True
        thread_first.start()
        thread_second.start()

        thread_first.join()
        thread_second.join()

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
