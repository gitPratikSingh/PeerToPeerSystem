from socket import*

class Server:
    clientList
    rfcList
    serverPort = 7734

    def __init__(self):
        self.serverSocket = self.listen()
        self.clientList = []
        self.rfcList = []

    def listen(self):
        server_socket = socket(AF_INET,SOCK_STREAM)
        server_socket.bind('',self.serverPort)
        server_socket.listen()
        print('The server is up!')
        return server_socket

    def OKconnect(self):
        msg = f'P2P-CI/1.0 200 OK'
        self.sendStream(msg)

    def BADREQUESTconnect(self):
        msg = f'P2P-CI/1.0 400 Bad Request'
        self.sendStream(msg)

    def OKadd(self):
        msg = ''

    def sendStream(self, msg):
        msg = raw_input(f'msg')
        self.clientSocket.send(msg)

    if __main__ == "__main__":
        server1 = Server()
        while 1:
            connectionSocket, addr = server1.serverSocket.accept()
            request = connectionSocket.recv(1024)
            parse = request.split('\n')
            if parse[0] != 'REGISTER':
                server1.BADREQUESTconnect()
                connectionSocket.close()
                break
            else:
                server1.OKconnect()
                
