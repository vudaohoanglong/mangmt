from tkinter.constants import FALSE, NO
from mysocket import MySocket
import mysocket as msk
from tkinter import messagebox
from scrshot_ui import scrshot_ui
from keystroke_ui import keystroke_ui
import tkinter as tk
import tkinter as tk
HOST = "127.0.0.1"
PORT = 65432

mainroot=tk.Tk()

class Main(tk.Frame):
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.is_connected=False
        self.master.title("Client")
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.master.resizable(False,False)
        self.grid()
        self.create_widgets()
        self.socket=None
        self.is_running=False
        self.subroot=[None]*2
    def create_widgets(self):
        self.entry=tk.Entry(width=50)
        self.entry.grid(row=0,column=0,columnspan=5,padx=10,pady=10)
        self.contents=tk.StringVar()
        self.contents.set("Nhập địa chỉ IP")
        self.entry["textvariable"]=self.contents
        self.Connect=tk.Button(text="Connect",width=10,height=1)
        self.Connect.grid(row=0,column=5,sticky=tk.NE,padx=10,pady=10)
        self.Connect['command']=self.connect
        self.Screenshot=tk.Button(text="ScreenShot",height=2,width=10)
        self.Screenshot.grid(row=1,column=0,sticky=tk.NW,padx=10,pady=10)
        self.Screenshot["command"]=self.create_screenshot
        self.Keystroke=tk.Button(text="KeyStroke",width=10,height=2)
        self.Keystroke.grid(row=2,column=0,sticky=tk.NW,padx=10,pady=10)
        self.Keystroke['command']=self.create_keystroke
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
    def create_keystroke(self):
        if self.check():
            return
        if not self.is_connected:
            messagebox.showerror("FAIL TO ATTEMPT","NOT CONNECTED YET")
            return
        self.socket.client.sendall(bytes("KEYSTROKE","utf8"))
        keystrokeroot=tk.Toplevel(self.master)
        self.subroot[0]=keystroke_ui(keystrokeroot,self.socket)
        self.subroot[0].mainloop()
    def create_screenshot(self):
        if self.check():
            return
        if not self.is_connected:
            messagebox.showerror("FAIL TO ATTEMPT","NOT CONNECTED YET")
            return
        self.socket.client.sendall(bytes("SCRSHOT","utf8"))
        screenshotroot=tk.Toplevel(self.master)
        self.subroot[1]=scrshot_ui(screenshotroot,self.socket)
        self.subroot[1].mainloop()
    def connect(self):
        strings=self.entry.get()
        if (self.is_connected):
            messagebox.showwarning("FAIL TO ATTEMPT","Already Connected")
            return
        #print(strings)
        try:
            self.socket=MySocket((strings,PORT))
            messagebox.showinfo("SUCCESS","Connected")
            self.is_connected=True
        except:
            messagebox.showerror("ERROR","Can not connect")
    def on_exit(self):
        if self.check():
            return
        try:
            self.socket.client.sendall(bytes("exit","utf8"))
        except:
            dem=1
        self.socket.close()
        self.master.destroy()
    def check(self):
        for i in range(2):
            if self.subroot[i] is not None and self.subroot[i].winfo_exists():
                return True
        return False
mainUI=Main(mainroot)
mainUI.mainloop()