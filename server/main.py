import socket 
import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab,Image
from keylog import Keylog
from registry import Registry
from process import Process
from app import App
import io
import os
HOST = ""
PORT = 65432
class Main(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.socket=None
        self.master.title("Server")
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.master.resizable(False,False)
        self.grid()
        self.is_opened=False
        self.conn=None
        self.create_widgets()
    def create_widgets(self):
        self.open=tk.Button(text='Mở',width=10,height=2)
        self.open.grid(column=0,row=0,padx=10,pady=10)
        self.open['command']=self.Open
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
    def Open(self):
        if self.is_opened:
            messagebox.showwarning('FAIL TO ATTEMPT',"OPENED ALREADY")
            return
        try:  
            self.is_opened=True
            self.socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)
            self.socket.bind((HOST,PORT))
            self.socket.listen(1)
            self.conn,self.addr=self.socket.accept()
            while True:
                bigcmd=str(self.conn.recv(4096).decode('utf8'))
                if (bigcmd=="SCRSHOT"):
                    while True:
                        cmd=str(self.conn.recv(4096).decode('utf8'))
                        if (cmd=="screen shot"):
                            img=ImageGrab.grab()

                            byteIO=io.BytesIO()

                            img.save(byteIO,format='BMP')

                            byteArr=byteIO.getvalue()
                            size = len(byteArr)

                            #print(size)
                            self.conn.sendall(bytes(str(size),'utf8'))
                            self.conn.sendall(byteArr)
                        elif cmd=="exit":
                            break
                elif (bigcmd=="KEYSTROKE"):
                    keystroke=Keylog(self.conn)
                    while True:
                        cmd=str(self.conn.recv(4096).decode('utf8'))
                        if (cmd=='hook'):
                            keystroke.hook()
                        elif cmd=='un_hook':
                            keystroke.un_hook()
                        elif cmd=='show':
                            keystroke.send_keys()
                        elif cmd=='delete':
                            keystroke.delete_keys()
                        elif cmd=='exit':
                            break
                elif bigcmd=="PROCESS":
                    process=Process(self.conn)
                    while True:
                        cmd=str(self.conn.recv(4096).decode('utf8'))
                        if (cmd=="view"):
                            process.process_view()
                        elif cmd=="kill":
                            while True:
                                id=str(self.conn.recv(4096).decode('utf8'))
                                if (id=="stopdoing"):
                                    break
                                else:
                                    process.process_kill(id)
                        elif cmd=="start":
                            while True:
                                id=str(self.conn.recv(4096).decode('utf8'))
                                if (id=="stopdoing"):
                                    break
                                else:
                                    process.process_start(id)
                        elif cmd=="exit":
                            break
                elif bigcmd=="APP":
                    app=App(self.conn)
                    while True:
                        cmd=str(self.conn.recv(4096).decode('utf8'))
                        if cmd=="view":
                            app.app_view()
                        elif cmd=="kill":
                            while True:
                                id=str(self.conn.recv(4096).decode('utf8'))
                                if (id=="stopdoing"):
                                    break
                                else:
                                    app.app_kill(id)
                        elif cmd=="start":
                            while True:
                                id=str(self.conn.recv(4096).decode('utf8'))
                                if (id=="stopdoing"):
                                    break
                                else:
                                    app.app_start(id)
                        elif cmd=="exit":
                            break
                elif bigcmd=="REGISTRY":
                    #print("haaha hahaha cc")
                    registry=Registry(self.conn)
                    registry.run_process()
                elif bigcmd=="SHUTDOWN":
                    os.system("shutdown /s /t 600")
                elif bigcmd=='exit':
                    self.is_opened=False
                    break
        except:
            messagebox.showwarning("ERROR","TIMEOUT CONNECTION")
            self.is_opened=False
            return
    def on_exit(self):
        if self.conn is not None:
            self.conn.close()
        self.master.destroy()
# ???????????????????????????
mainroot=tk.Tk()
mainUI=Main(mainroot)
mainUI.mainloop()
