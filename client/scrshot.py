from PIL import Image
import mysocket as msk
import io
class SCRSHOT:
    def __init__(self,sk):
        self.sk=sk
        self.img=None
        self.img_data=None
    def takePic(self):
        size=int(self.sk.client.recv(1024).decode('utf8'))
        #self.sk.client.sendall(bytes("got it",'utf8'))
        photo=b''
        while size>0:
            data=self.sk.client.recv(4096)
            size-=len(data)
            photo+=data
        stream=io.BytesIO(photo)
        self.img_data=photo
        self.img=Image.open(stream)
        #self.img.show()
