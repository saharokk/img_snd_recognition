import cv2
import numpy as np
from PIL import Image, ImageTk



class faceLogic(object):
    _face_cascade = None
    def __init__(self, face_cascade_path=None):
        self._frame = None # frame/image var
        self.cap = cv2.VideoCapture(0)
        self.scaling_factor = 1.5
        self._facesNum = 0

        if face_cascade_path:
            self._face_cascade = cv2.CascadeClassifier(face_cascade_path)
            if self._face_cascade.empty():
                raise IOError('Unable to load the face cascade classifier xml file')
    def getFrame(self):
        #convert to true RGB
        return cv2.cvtColor(self._frame, cv2.COLOR_BGR2RGB) 

    def getTkImg(self):
        img = ImageTk.PhotoImage(image=Image.fromarray(self._frame))
        return img
    def capFrame(self):
        """Capture feame from capture device"""
        _, self._frame = self.cap.read()

    def getFacesNum(self):
        return self._facesNum

    def findFace(self):
        """CV2 routine to find face from np.ndarray as image"""
        if not self._frame.any():
            raise fAppException("Attempt to proccess None frame!")
        self._frame = cv2.resize(self._frame, None, 
            fx=self.scaling_factor, 
            fy=self.scaling_factor, 
            interpolation=cv2.INTER_AREA)

        # Converting to greyscale
        gray = cv2.cvtColor(self._frame, cv2.COLOR_BGR2GRAY)

        # Face detection
        face_rects = self._face_cascade.detectMultiScale(gray, 1.3, 5)
        if not str(type(face_rects)) == "<class 'tuple'>":
            self._facesNum = face_rects.size/4
        else:
            self._facesNum = 0

        k, l = 0, 0
            # Draw rects around faces
        for (x,y,w,h) in face_rects:
            cv2.rectangle(self._frame, (x,y), (x+w,y+h), (0,255,0), 3)
            k = x
            l = y

    def applyCounter(self):
            cv2.putText(self._frame, ('Faces in frame: %d'%self._facesNum), (40,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,255,100), 2)


    def readByPath(self, path=None):
        if not path:
            raise fAppException("No image path specified!")
        else:
            self._frame = cv2.imread(path)
        
    def __del__(self):
        self.cap.release()
        
class fAppException(Exception):
    def __init__(self, message):
        super().__init__(message)