import tkinter as tk
from scrshot import SCRSHOT
from PIL import Image,ImageTk
from tkinter import messagebox,filedialog
import io
class scrshot_ui(tk.Frame):
    def __init__(self, master=None,sk=None):
        super().__init__(master)
        self.master = master
        self.master.title("Screen Shot")
        self.master.grid_rowconfigure(0,weight=1)
        self.master.grid_columnconfigure(0,weight=1)
        self.grid()
        self.create_widgets()
        self.scr=SCRSHOT(sk)
    def create_widgets(self):
        self.canvas=tk.Canvas(self,width=560,height=500)
        self.item_on_canvas=self.canvas.create_image(280,280,anchor=tk.CENTER,image=None)
        self.canvas.grid(row=0,column=0,sticky=tk.NW,padx=10,pady=10,rowspan=1)
        self.snip=tk.Button(self,text='Chụp',width=20,height=10)
        self.snip.grid(row=0,column=1,sticky=tk.E,padx=10,pady=10)
        self.snip['command']=self.screenshot
        self.save=tk.Button(self,text='Lưu',width=20,height=10)
        self.save.grid(row=1,column=1,sticky=tk.E,padx=10,pady=10)
        self.save['command']=self.savescreen
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)
    def _resize_image(self, IMG):
        h = w = 0

        basewidth = 560
        wpercent = basewidth / float(IMG.size[0])
        hsize = int((float(IMG.size[1]) * float(wpercent)))

        if (hsize > 560):
            h = 560
            hpercent = h / float(hsize)
            w = int((float(basewidth) * float(hpercent)))
        else:
            h = hsize
            w = basewidth

        return IMG.resize((int(w), int(h)), Image.ANTIALIAS)
    def screenshot(self):
        self.scr.sk.client.sendall(bytes("screen shot","utf8"))
        self.scr.takePic()
        self._img = ImageTk.PhotoImage(self._resize_image(self.scr.img))
        self.canvas.itemconfig(self.item_on_canvas, image=self._img)
        self.update_idletasks()
        self.update()
    def savescreen(self):
        if self.scr.img_data == None:
            messagebox.showerror("Screenshot", "Can not save image")
            return
        files = [('PNG', '*.png'),
                 ('JPEG', '.jpg;.jpeg')]
        file= filedialog.asksaveasfile(
            mode="wb", filetypes=files, defaultextension=files, title="Save image")
        if file != None:
            file.write(self.scr.img_data)
            file.close()
    def on_exit(self):
        self.scr.sk.client.sendall(bytes("exit","utf8"))
        #self.scr.sk.close()
        self.master.destroy()