import os 
import socket 

class Process:
    def __init__(self,sk):
        self.sk=sk 
    def process_view(self):
        output = os.popen('powershell "gps |  select name, id, {$_.Threads.Count}').read()
        self.sk.sendall(bytes(str(len(output)),"utf8"))
        self.sk.sendall(bytes(output,"utf8"))