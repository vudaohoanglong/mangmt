from tkinter import EXCEPTION
from tkinter.constants import E, NONE
import winreg 
import os
import socket 

class Registry:
    def __init__(self,socket=None):
        self.socket=socket
        pass
    def run_process(self):
        while True:
            cmd=str(self.socket.recv(4096).decode("utf8"))
            if cmd=="file":
                self.update_regfile()
            elif cmd=="exit":
                try:
                    os.remove("Regfile.reg")
                except:
                    pass 
                return
            else:
                tmp=len(cmd.split(","))
                if tmp!=5:
                    print(1)
                    continue
                cmd,path,name,value,datatype=cmd.rsplit(",",4)
                path=path.replace("/","\\")
                if (len(path.split("\\",1)==2)):
                    HKEY,link=path.split("\\",1)
                else:
                    HKEY,link=path,""
                HKEY=self.registyKey(HKEY)
                datatype=self.registryData(datatype)
                if HKEY is None:
                    self.socket.send(bytes("HKEY NOT FOUND","utf8"))
                    continue
                reg=winreg.ConnectRegistry(None,HKEY)
                if (cmd=="Get value"):
                    self.get_value(reg,link,name)
                elif cmd=="Set value":
                    self.set_value(reg,link,name,value,datatype)
                elif cmd=="Delete value":
                    self.delete_value(reg,link,name)
                elif cmd=="Create key":
                    self.create_key(reg,link)
                elif cmd=="Delete key":
                    self.delete_key(reg,link)
    def update_regfile(self):
        lenFile=int(self.socket.recv(4096).decode("utf8"))
        strings=b""
        while lenFile>0:
            data=self.socket.recv(4096).decode("utf8")
            strings+=data
            lenFile-=len(data)
        content=strings.decode("utf8")
        file=open("Regfile.reg","w")
        file.write(strings)
        file.close()
        try:
            os.popen("regedit.exe /s Regfile.reg")
        except Exception:
            self.socket.send(bytes("FAIL","utf8"))
            os.remove("Regfile.reg")
            return
        self.socket.send(bytes("SUCCESS","utf8"))
    def get_value(self,reg,link,name):
        try:
            key=winreg.OpenKey(reg,link,0,winreg.KEY_QUERY_VALUE)
            result=winreg.QueryValueEx(key,name)
            if not result[0]:
                data="Error"
            else:
                if result[1]==winreg.REG_MULTI_SZ:
                    data=""
                    for x in result[0]:
                        data=data+x+"\n"
                elif result[1]==winreg.REG_BINARY:
                    data=" ".join("%02x" % x for x in result[0])
                else:
                    data=str(result[0])
                self.socket.sendall(bytes(data,"utf8"))
                winreg.CloseKey(key)
        except Exception:
            self.socket.sendall(bytes("Error","utf8"))
            return
    def set_value(self,reg,link,name,value,datatype):
        try:
            if datatype in [winreg.REG_DWORD,winreg.REG_QWORD]:
                value=int(value)
            elif datatype==winreg.REG_MULTI_SZ:
                value=value.split("\n")
            elif datatype==winreg.REG_BINARY:
                value=value.replace(" ","")
                value=bytearray.fromhex(value)
            key=winreg.OpenKey(reg,link,0,winreg.KEY_SET_VALUE) 
            winreg.SetValueEx(key,name,0,datatype,value)
            winreg.CloseKey(key)
        except Exception:
            self.socket.send(bytes("Error",'utf8'))
            return
        self.socket.send(bytes("Set key successfully","utf8"))
    def delete_value(self,reg,link,name):
        try:
            key=winreg.OpenKey(reg,link,0,winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key,name)
        except:
            self.socket.send(bytes("Error","utf8"))
            return
        self.socket.send(bytes("delete value successfully","utf8"))
    def create_key(self,reg,link):
        try:
            winreg.CreateKey(reg,link)
        except Exception:
            self.socket.send(bytes("Error","utf8"))
            return
        self.socket.send(bytes("Create key successfully","utf8"))
    def delete_key(self,reg,link):
        try:
            winreg.DeleteKey(reg,link)
        except Exception:
            self.socket.send(bytes("Error",'utf8'))
            return
        self.socket.send(bytes("Delete key successfully","utf8"))

    def registryKey(self,name):
        if (len(name) == 0):
            return None
        if name == "HKEY_CLASSES_ROOT":
            return winreg.HKEY_CLASSES_ROOT
        elif name == "HKEY_CURRENT_USER":
            return winreg.HKEY_CURRENT_USER
        elif name == "HKEY_LOCAL_MACHINE":
            return winreg.HKEY_LOCAL_MACHINE
        elif name == "HKEY_USERS":
            return winreg.HKEY_USERS
        elif name == "HKEY_CURRENT_CONFIG":
            return winreg.HKEY_CURRENT_CONFIG
        else:
            return None
    def registryData(self, name):
        if len(name) == 0:
            return None
        if name == "String":
            return winreg.REG_SZ
        elif name == "Binary":
            return winreg.REG_BINARY
        elif name == "DWORD":
            return winreg.REG_DWORD
        elif name == "QWORD":
            return winreg.REG_QWORD
        elif name == "Multi-String":
            return winreg.REG_MULTI_SZ
        elif name == "Expandable string":
            return winreg.REG_EXPAND_SZ
        else:
            return None
