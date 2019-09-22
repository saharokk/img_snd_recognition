from tkinter import *
from tkinter import filedialog
from faceLogic import *
from PIL import Image, ImageTk
import time 

class faceApp(Frame):
    layout = "cam"
    modeBtnTxt = None
    faceAppHndlr = None
    camDelay = 30 # FPS = 1/camDelay

    def __init__(self, parent):
        Frame.__init__(self, parent)

        # Add a mode select button with changable text on ot
        self.modeBtnTxt = StringVar(value="Switch to File mode")
        self.modeSelectBtn = Button(self, textvariable=self.modeBtnTxt, command=self.switch_layout)
        self.modeSelectBtn.grid(row=0, column=0)

        
        self.openFileBtn = Button(self, text="Open image", command=self.open_image)

        self.place(x=25, y=20)  
        self.label = Label(self)#, width=self.winfo_width(), height=(self.winfo_height()-100) )#Frame(self, width=700, height=500) 
        self.label.grid(row=2, column=0)
       
        self.fLogic = faceLogic(face_cascade_path='C:\\Users\\dsakharov.cw\\Documents\\KNU\\image_&_sound_recognition\\lab2\\haarcascade_frontalface_default.xml')
        self.update_window()

    def switch_layout(self):
        if self.layout == "cam":
            self.layout = "file"
            self.initFileMode()
        else:
            self.layout = "cam"
            self.initCamMode()


        print("Current layout is %s" % self.layout)
    
    def initCamMode(self):
        self.modeBtnTxt.set("Switch to file mode")
        self.openFileBtn.grid_remove()
        self.update_window()

        
    def initFileMode(self):
        self.modeBtnTxt.set("Switch to Camera mode")
        self.openFileBtn.grid(row=1, column=0)
    
    def open_image(self):
        filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
        self.fLogic.readByPath(filename)
        self.update_window()
        
    def update_window(self):

        if self.layout == "cam":
            self.fLogic.capFrame()
        if not self.fLogic.getFrame().any():
            raise fAppException("None frame")
        self.fLogic.findFace()
        if self.layout == "cam":
            self.fLogic.applyCounter()
        
        frame = self.fLogic.getFrame()
    
        Tk.update(self)
        img = Image.fromarray(frame).resize( (640, 480), resample=Image.LANCZOS)
        img = ImageTk.PhotoImage(image=img)
        self.label.imgtk = img
        self.label.configure(image=img)

        if self.layout == "cam":
            self.label.after(self.camDelay, self.update_window)

root = Tk()
root.geometry()
root.minsize(width=700, height=600)
#root.resizable(0,0)
#root.config(background="#FFFFFF")
fApp = faceApp(root)
fApp.mainloop()