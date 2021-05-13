import socket 

class MySocket:
    def __init__(self,sv_adress):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client.connect(sv_adress)
    def close(self):
        self.client.close()
