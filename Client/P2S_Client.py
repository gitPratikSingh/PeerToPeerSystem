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
        print("")

    def sendRegisterMessage(self):
        # request
        msg = f'REGISTER P2P-CI/1.0 \nHost: {self.hostName} \nPort: {self.uploadPort} \n'
        print("Inside Register Client,msg: ")
        print(msg)
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
        msg = ''
        for rfc in P2P_Client.rfcList:
            msg = msg + self.ADD(rfc)
        return msg

    def sendStream(self, msg):
        print(msg)
        self.clientSocket.send(msg.encode('utf-8'))

    def recvStream(self):
        msg = self.clientSocket.recv(1024)
        return msg.decode('utf-8')

    def ADD(self, rfc):
        # request
        msg = f'ADD RFC {rfc[0]} P2P-CI/1.0\nHost: {self.hostName}\nPort: {self.hostPort}\nTitle: {rfc[1]}\n'
        self.sendStream(msg)

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
        file_name = str(rfc_number) + "-" + rfc_title + ".txt"

        peer_socket.send(message)
        reply = peer_socket.recv(1024)

        reply_list = re.split(reply)
        os.chdir(os.getcwd())

        if str(reply_list[1]) == '200':

            rfc_file = open(file_name, 'wb')
            while True:
                recv_rfc_data = peer_socket.recv(1024)
                if recv_rfc_data:
                    rfc_file.write(recv_rfc_data)
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
            rfc_number = int(input())
            print("Enter the title for the RFC")
            rfc_title = input()
            print("Enter Peer's Hostname")
            peer_host_name = input()
            print("Enter Peer port number")
            port_peer = int(input())

            p2p_client.GET_RFC(rfc_number, rfc_title, peer_host_name, port_peer)

        if choice == 5:
            p2p_client.REMOVE_CLIENT()



def main():
    #print("Enter IP address of the host")
    #IP = input()
    #print("Enter Host name")
    #HOST = input()
    #print("Enter Upload Port number")
    #PORT = int(input())

    IP = '127.0.0.1'
    HOST = 'localhost'
    PORT = 12345
    p2p_client = P2P_Client(HOST, IP, PORT)

    try:
        print("In main")
        # thread_first = threading.Thread(target=p2p_client.p2p_server.p2p_server_start)
        thread_second = threading.Thread(target=menu, args=(p2p_client,))
        # thread_first.daemon = True
        thread_second.daemon = True
        # thread_first.start()
        thread_second.start()

        # thread_first.join()
        thread_second.join()

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
