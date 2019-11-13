import cv2
import threading
from time import sleep
from PyQt5 import QtCore
from PyQt5.QtGui import QImage, QPixmap


class Camera(QtCore.QThread):

    frame_is_ready = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.camera_list = []
        self.frame = None
        self.capture = None
        self.init_select_camera()

        # Variants
        self.resolution = None
        # Threads

        self.e2 = threading.Event()
        self.e2.clear()
        self.e1 = threading.Event()
        self.e1.clear()
        self.e1.set()

    def run(self):
        while True:
            self.e1.wait()
            ret, frame = self.capture.read()
            self.frame = frame.copy()
            self.e2.set()
            self.frame_is_ready.emit(frame)

    def init_select_camera(self):
        def get_list():
            cameras = []
            for i in range(3):
                try:
                    capture = cv2.VideoCapture(i)
                    r, loc_img = capture.read()
                    if loc_img is None:
                        break
                    else:
                        cameras.append(str(i))
                    capture.release()
                    continue
                except:
                    print("there are only {} available cameras".format(len(cameras)))
                    break
            return cameras

        self.camera_list = get_list()
        try:
            self.capture = cv2.VideoCapture(int(self.camera_list[-1]))
        except:
            self.capture = cv2.VideoCapture(int(self.camera_list[0]))

    def select_camera(self, camera_n):
        n = int(camera_n)
        self.e1.clear()
        sleep(0.1)
        self.capture.release()
        self.capture = cv2.VideoCapture(int(self.camera_list[n]))
        self.e1.set()

    def select_settings(self,camera_n,resX,resY,fps):
        self.e1.clear()
        sleep(1)
        self.capture.release()
        self.capture = cv2.VideoCapture(int(self.camera_list[int(camera_n)]))
        self.capture.set(3,resY)
        self.capture.set(4,resX)
        self.capture.set(5,fps)
        self.e1.set()

    def modes(self):
        import pandas as pd
        from os import getcwd
        path = '{}\scanner\camera\camera modes\BRIO.xlsx'.format(getcwd())
        df = pd.read_excel(path)
        return df
        
if __name__ == "__main__":
    # c = Camera()
    # a = c.camera_list

    pass
