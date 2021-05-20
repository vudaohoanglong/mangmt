import tkinter as tk
import sys 
import os 
import codecs
from tkinter import Message, filedialog,messagebox
from tkinter.constants import S
from typing import Counter, DefaultDict
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
        self.regpath = ""
        self.regcontent = tk.StringVar(self)
        self.regcontent.set("")
        self.result=""
        self.create_widgets()
    def create_widgets(self):
        #Thay doi tu file .reg
        self.txt_regpath=tk.Text(self,width=64,height=2,bg='#FFFFFF')
        self.txt_regpath.grid(row=0,column=0,sticky=tk.N,padx=10,pady=10,columnspan=3)
        self.btn_browse=tk.Button(self,text='Browse',width=30,height=2)
        self.btn_browse.grid(row=0,column=3,sticky=tk.N,pady=10,padx=10)
        self.btn_browse["command"]=self.browser_path
        self.reg_box_text=tk.Text(self,width=64,height=10,bg="#FFFFFF")
        self.reg_box_text.grid(row=1,column=0,columnspan=3,sticky=tk.N,padx=10,pady=10)
        self.btn_send_cnt=tk.Button(self,text='Gửi nội dung',wraplength=50,width=30,height=10)
        self.btn_send_cnt.grid(row=1,column=3,sticky=tk.N,padx=10,pady=10)
        self.btn_send_cnt["command"]=self.send_reg_file
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
        self.lb_type=tk.Label(self,text="Data type",height=1,justify=tk.CENTER)
        self.lb_type.grid(row=5,column=3,sticky=tk.N,padx=10,pady=10,columnspan=2)
        self_types={"String","Binary","DWORD","QWORD","Multi-String","Expandable string"}
        self.default_type=tk.StringVar(self)
        self.default_type.set("String")
        self.option_type=tk.OptionMenu(self,self.default_type,*self_types)
        self.option_type.config(width=25)
        self.option_type.grid(row=6,column=3,columnspan=1,pady=10,padx=10,sticky=tk.N)
        #Textbox_result
        self.text_result=tk.Text(self,width=88,height=15,state="disable",bg="#FFFFFF")
        self.text_result.grid(row=7,column=0,columnspan=4,sticky=tk.N,padx=10,pady=10)
        #Gui va xoa 
        self.btn_send=tk.Button(self,text="Gửi",width=20,height=2)
        self.btn_send.grid(row=8,column=0,sticky=tk.N,pady=10,padx=10,columnspan=2)
        self.btn_send["command"]=self.send_reg_direct
        self.btn_delete=tk.Button(self,text="Xóa",width=20,height=2)
        self.btn_delete.grid(row=8,column=2,sticky=tk.N,padx=10,pady=10,columnspan=2)
        self.btn_delete["command"]=self.clear_result
        #chon chuc nang
        self.lb_func=tk.Label(self,text="Chức năng:",width=25,height=1,justify=tk.LEFT)
        self.lb_func.grid(row=3,column=0,columnspan=1,sticky=tk.E,padx=10,pady=10)   
        self.func={"Set value","Get value","Delete key","Create key","Delete value"}     
        self.df_func=tk.StringVar(self)
        self.df_func.trace("w",lambda a,b,c :self.update_ui(a=a,b=b,c=c))
        self.df_func.set("Get value")
        
        self.option_func=tk.OptionMenu(self,self.df_func,*self.func)
        self.option_func.grid(row=3,column=1,sticky=tk.W,padx=10,pady=10,columnspan=3)
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
    def update_ui(self,a,b,c):
        if self.df_func.get()=="Set value":
            self.lb_name.grid()
            self.txt_name.grid()
            self.lb_value.grid()
            self.txt_value.grid()
            self.lb_type.grid()
            self.option_type.grid()
        else:
            self.lb_value.grid_remove()
            self.txt_value.grid_remove()
            self.lb_type.grid_remove()
            self.option_type.grid_remove()
            if self.df_func.get() in {"Create key","Delete key"}:
                self.lb_name.grid_remove()
                self.txt_name.grid_remove()
            else:
                self.lb_name.grid()
                self.txt_name.grid()
    def send_reg_file(self):
        strings=self.reg_box_text.get("1.0",tk.END).strip("\n")
        #print(strings)
        self.socket.client.send(bytes("file","utf8"))
        self.socket.client.send(bytes(str(len(strings)),"utf8"))
        self.socket.client.sendall(bytes(strings,"utf8"))
        result=str(self.socket.client.recv(4096).decode("utf8"))
        self.insert_result(result)
    def send_reg_direct(self):
        strings=self.df_func.get()+','+self.txt_path.get("1.0",tk.END).strip("\n")+","+ self.txt_name.get("1.0",tk.END).strip("\n")+","+self.txt_value.get("1.0",tk.END).strip("\n")+","+self.default_type.get()
        #print(strings)
        self.socket.client.sendall(bytes(strings,"utf8"))
        result=str(self.socket.client.recv(4096).decode("utf8"))
        self.insert_result(result)
    def browser_path(self):
        files = [('Registry Files', '*.reg'),
                 ('Text Documents', '*.txt'), ('All files', '*')]
        self.regpath=filedialog.askopenfilename(filetype=files,defaultextension=files,title="Open file")
        self.txt_regpath.delete("1.0",tk.END)
        self.txt_regpath.insert("end",self.regpath)
        self.update_content()
    def update_content(self):
        try:
            file=codecs.open(filename=self.regpath,mode="r",encoding="utf-16")
            self.regcontent=file.read()
            self.reg_box_text.delete("1.0",tk.END)
            self.reg_box_text.insert("end",self.regcontent)
        except:
            messagebox.showerror("error","file does not exist")
            self.txt_regpath.delete("1.0",tk.END)
    def insert_result(self, result="Lỗi"):
        self._response = result.strip("\n")
        self._response += "\n"
        self.text_result.configure(state="normal")
        self.text_result.insert("end", self._response)
        self.text_result.configure(state="disable")
    def clear_result(self):
        self.text_result.configure(state="normal")
        self.text_result.delete("1.0", tk.END)
        self.text_result.configure(state="disable")
    def on_exit(self):
        self.socket.client.sendall(bytes("exit","utf8"))
        self.master.destroy()
