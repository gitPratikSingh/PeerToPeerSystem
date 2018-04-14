import socket
import threading
import re

class P2P_Server():

    def __init__(self, hostName, hostip, uploadPort):
        self.hostname = hostName
        self.hostip = hostip
        self.uploadPort = uploadPort

    def p2p_server_start(self):

        client_socket = socket.socket()
        client_socket.bind((self.hostip,self.uploadPort))
        client_socket.listen(2)

        print("Started listening for" + str(client_socket))
        while(1):

            (peer_socket,peer_addr)=client_socket.accept()
            print("Connected to"+ str(peer_addr))

            thread=threading.Thread(target=self.sendRFC,args=("sendRFC",peer_socket))
            thread.start()
            thread.join()

        client_socket.close()
        return

    def sendRFC(self, name, sock):
        request=sock.recv(1024)
        print (request)

        rfc_number=re.split(request)
        file_found = 0

        for x in rfc_number:
            t = x.split("-")
            if int(t[0])==int(rfc_number[2]):
                print (t[0])
                file_found=1
                file_name=str(x)+".txt"

        if file_found==0:
            print("File not found")
            file_data="P2P-CI/1.0 404 FILE NOT FOuND"+"\n"
            sock.send(file_data)
        else:
            file_data="P2P-CI/1.0 200 OK"+"\n"
            sock.send(file_data)

            with open(file_name,'r') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)

        sock.close()



if __name__ == "__main__":
    hostName = 'localhost'
    hostip='127.0.0.1'
    uploadPort=10001
    p2p_Server = P2P_Server(hostName, hostip, uploadPort)
    p2p_Server.p2p_server_start()