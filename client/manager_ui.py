import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from mysocket import MySocket
class Entry_ui(tk.Frame):
    def __init__(self,master=None,sk=None,name=None):
        super().__init__(master)
        self.master=master
        self.name=name
        self.sk=sk
        self.master.title(name)
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.master.resizable(False,False)
        self.grid()
        self.create_widgets()
    def create_widgets(self):
        self.entry=tk.Entry(self,width=50)
        self.entry.grid(row=0,column=0,columnspan=5,padx=10,pady=10)
        self.contents=tk.StringVar(self)
        if (self.name=="kill"): self.contents.set("Nhập ID")
        elif self.name=="start": self.contents.set("Nhập tên")
        self.entry["textvariable"]=self.contents
        self.Connect=tk.Button(self,text=self.name,width=10,height=1)
        self.Connect.grid(row=0,column=5,sticky=tk.NE,padx=10,pady=10)
        self.Connect['command']=self.connect
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
    def connect(self):
        strings=self.entry.get()
        self.sk.client.sendall(bytes(strings,"utf8"))
        result=str(self.sk.client.recv(4096).decode("utf8"))
        messagebox.showinfo(result,result)
    def on_exit(self):
        self.sk.client.sendall(bytes("stopdoing","utf8"))
        self.master.destroy()

class Manager_ui(tk.Frame):
    def __init__(self,master=None,sk=None,name=None):
        super().__init__(master)
        self.master=master
        self.sk=sk
        self.name=name
        self.master.title(name)
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.master.resizable(False,False)
        self.grid()
        self.create_widgets()
        self.subroot=None
    def create_widgets(self):
        self.View=tk.Button(self,text="View",width=10,height=5)
        self.View.grid(column=0,row=0,padx=10,pady=10)
        self.View['command']=self.view_func
        self.Kill=tk.Button(self,text="Kill",width=10,height=5)
        self.Kill.grid(column=1,row=0,padx=10,pady=10)
        self.Kill['command']=self.kill_func
        self.Start=tk.Button(self,text="Start",width=10,height=5)
        self.Start.grid(column=2,row=0,pady=10,padx=10)
        self.Start["command"]=self.start_func
        self.Delete=tk.Button(self,text="Delete",width=10,height=5)
        self.Delete.grid(column=3,row=0,padx=10,pady=10)
        self.Delete["command"]=self.cleartable
        cols = ("Name " + self.name, "ID " + self.name, "Threads count")
        self.table = ttk.Treeview(self, columns=cols, show="headings")
        self.table.grid(row=1, column=0, sticky=tk.N,
                        padx=10, pady=10, columnspan=4)
        for col in cols:
            self.table.heading(col, text=col)
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
    def start_func(self):
        if self.check():
            return
        self.sk.client.sendall(bytes("start","utf8"))
        startroot=tk.Toplevel(self.master)
        self.subroot=Entry_ui(startroot,self.sk,"start")
        self.subroot.mainloop()
    def kill_func(self):
        if self.check():
            return
        self.sk.client.sendall(bytes("kill","utf8"))
        startroot=tk.Toplevel(self.master)
        self.subroot=Entry_ui(startroot,self.sk,"kill")
        self.subroot.mainloop()
    def view_func(self):
        if self.check():
            return
        self.sk.client.sendall(bytes("view","utf8"))
        size=int(self.sk.client.recv(4096).decode("utf8"))
        strings=b""
        while size>0:
            data=self.sk.client.recv(4096)
            strings+=data
            size-=len(data)
        table=str(strings.decode("utf8"))
        self.showdata(table)
    def showdata(self, data):
        self.cleartable()
        if (data):
            data = data.split('\n')[3:-3]  
            data.sort(key=lambda x: x[0].upper())  
        for current_process in data:
            (name_process, id_process, count_thread) = current_process.rsplit(maxsplit=2)
            self.table.insert("", "end", values=(
                name_process, id_process, count_thread))
    def cleartable(self):
        for rowid in self.table.get_children():
            self.table.delete(rowid)
    def on_exit(self):
        if self.check():
            return
        self.sk.client.sendall(bytes("exit","utf8"))
        self.master.destroy()
    def check(self):
        if self.subroot is not None and self.subroot.winfo_exists():
            return True
        return False

