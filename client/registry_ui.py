import tkinter as tk
import sys 
import os 
import codecs
from typing import Counter
import mysocket as msk

class Registry_UI(tk.Frame):
    def __init__(self,master=None,socket=None):
        super().__init__(master)
        self.master=master
        self.socket=socket
        self.master.title("Registry")
        self.master.resizable(False, False)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)
        self.grid()
        self.create_widgets()
    def create_widgets(self):
        #Thay doi tu file .reg
        self.txt_path=tk.Text(self,width=64,height=2,bg='#FFFFFF')
        self.txt_path.grid(row=0,column=0,sticky=tk.N,padx=10,pady=10,columnspan=3)
        self.btn_browse=tk.Button(self,text='Browse',width=30,height=2)
        self.btn_browse.grid(row=0,column=3,sticky=tk.N,pady=10,padx=10)
        self.reg_box_text=tk.Text(self,width=64,height=10,bg="#FFFFFF")
        self.reg_box_text.grid(row=1,column=0,columnspan=3,sticky=tk.N,padx=10,pady=10)
        self.btn_send=tk.Button(self,text='Gửi nội dung',wraplength=50,width=30,height=10)
        self.btn_send.grid(row=1,column=3,sticky=tk.N,padx=10,pady=10)
        #break-line
        self.breakline=tk.Label(self,text="-"*30+"Sửa giá trị trực tiếp"+"-"*30,height=1,justify=tk.CENTER)
        self.breakline.grid(row=2,column=0,sticky=tk.N,padx=10,pady=10,columnspan=4)
        #Thay doi truc tiep
        #path
        self.lb_path=tk.Label(self,text="Đường dẫn",width=20,justify=tk.CENTER)
        self.lb_path.grid(row=4,column=0,sticky=tk.E,padx=10,pady=10,columnspan=1)
        self.txt_path=tk.Text(self,width=50,height=1,bg="#FFFFFF")
        self.txt_path.grid(row=4,column=1,columnspan=3,sticky=tk.W,padx=10,pady=10)
        #Name value
        self.lb_name=tk.Label(self,text="Name value",height=1,justify=tk.CENTER)
        self.lb_name.grid(row=5,column=0,sticky=tk.N,padx=10,pady=10,columnspan=1)
        self.txt_name=tk.Text(self,width=25,height=1,bg="#FFFFFF")
        self.txt_name.grid(row=6,column=0,sticky=tk.N,columnspan=1,pady=10,padx=10)
        #Value settings
        self.lb_value=tk.Label(self,text="Value",height=1,justify=tk.CENTER)
        self.lb_value.grid(row=5,column=1,sticky=tk.N,padx=10,pady=10,columnspan=2)
        self.txt_value=tk.Text(self,width=25,height=1,bg="#FFFFFF")
        self.txt_value.grid(row=6,column=1,sticky=tk.N,pady=10,padx=10,columnspan=2)
        #Select type
        self.lb_type=tk.Label(self,)
root=tk.Tk()
app=Registry_UI(root)
app.mainloop()
