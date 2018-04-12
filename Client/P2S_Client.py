import socket
import threading
import os
from P2P_Server import *

class P2P_Client():
    rfcList=list() #List of lists [[RFC#, RFC_TITLE]]
    serverPort = 7734 #predefined port number for server
    serverName = 'localhost' #should be predefined later

    def __init__(self, hostName, hostip, uploadPort):
        self.hostName = hostName
        self.uploadPort = uploadPort
		self.hostIP = hostip
        self.fetchLocalRFCs()
        self.connectServer()
		self.sendRegisterMessage()
        self.sendRFCList()
		self.p2p_server = P2P_Server(hostName, hostip, uploadPort)

    def fecthLocalRFCs(self):
        # to be implemented
        # returns a list of the existing RFCs
        # read data directory and set rfcList


	def sendRegisterMessage(self):
		# request
		msg = f'REGISTER P2P-CI/1.0 \n Host: {self.hostName} \n Port: {self.uploadPort} \n'
		self.sendStream()
		
		#response
		recvmsg = self.recvStream()
        print(recvmsg)
	
    def connectServer(self):
		global serverName
		global serverPort
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect(serverName, serverPort)

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
		
	def GET_RFC(rfc_number, rfc_title, peer_host_name,port_peer):
		peer_socket=socket.socket()
		peer_socket.connect((peer_host_name,port_peer))
		print "P2S connected"
		
		message="GET RFC"+" "+str(rfc_number)+" "+"P2P-CI/1.0"+"\n"+"Host: "+peer_host_name+"\n"+"OS: Windows \n"
        file_name=str(rfc_number)+"-"+rfc_title+".txt"
            
		peer_socket.send(message)
		reply=peer_socket.recv(1024)
		
		reply_list=re.split(reply)
		os.chdir(os.getcwd())
				
		if str(reply_list[1])=='200':
			rfc_file=open(file_name,'wb')
			while True:
				recv_rfc_data=peer_socket.recv(1024)
				if recv_rfc_data:
					rfc_file.write(recv_rfc_data)
				else:
					rfc_file.close()
		else:
			print "File Not Found"
			
		peer_socket.close()
		
	def REMOVE_CLIENT(self):
		msg="REMOVE P2P-CI/1.0 Host: "+self.hostName+"\n"
		self.sendStream(msg)
		# response
        recvmsg = self.recvStream()
        print(recvmsg)
	
def menu(HOST, IP, PORT):
    
    p2p_client = P2P_Client(HOST, IP, PORT)

	while(1):
        print "Select from the List"
        print "1. List all RFC"
        print "2. Lookup RFC"
        print "3. Add RFC"
        print "4. Get RFC file"
        print "5. Exit"
        print "6. Remove a RFC"

        choice=int(raw_input())
        
        if choice==1:
            p2p_client.LIST()
            
        if choice==2:
            print "Enter RFC number"
            rfc_number = int(raw_input())
            print "Enter RFC title"
            rfc_title=raw_input()
			
			rfc = list()
			rfc.append(rfc_number)
			rfc.append(rfc_title)
			
            p2p_client.LOOKUP(rfc)
			
        if choice==3:
            print "Enter RFC number"
            rfc_number=raw_input()
            print "Enter the title for the RFC"
            rfc_title=raw_input()
            
			rfc = list()
			rfc.append(rfc_number)
			rfc.append(rfc_title)
			
			p2p_client.ADD(rfc)
                
        if choice==4:
            print "Enter RFC number"
            rfc_number=int(raw_input())
            print "Enter the title for the RFC"
            rfc_title=raw_input()
            print "Enter Peer's Hostname"
            peer_host_name=raw_input()
            print "Enter Peer port number"
            port_peer=int(raw_input()) 
			
            p2p_client.GET_RFC(rfc_number, rfc_title, peer_host_name,port_peer)

        if choice==5:
            p2p_client.REMOVE_CLIENT()

    return 
	
def main():

    print "Enter IP address of the host"
    IP=raw_input()
    print "Enter Host name"
    HOST=raw_input()
    print "Enter Upload Port number"
    PORT=int(raw_input())

    try:
        thread_first = threading.Thread(target=self.p2p_server.p2p_server_start)
        thread_second = threading.Thread(target=self.menu, args=(HOST, IP, PORT))
        thread_first.daemon=True
        thread_second.daemon=True
        thread_first.start()
        thread_second.start()

        thread_first.join()
        thread_second.join()

    except KeyboardInterrupt:
        sys.exit(0)