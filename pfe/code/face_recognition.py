from PyQt5 import QtCore, QtGui, QtWidgets
import cv2, time, reconGUI, os, pickle
from PyQt5.QtWidgets import QMessageBox


class Thread(QtCore.QThread):
    frameItem = QtCore.pyqtSignal(QtWidgets.QGraphicsPixmapItem)
    person = QtCore.pyqtSignal(str)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.ret = True
        self.vid_name = 0
        self.play_speed = 0.03
        self.fr_proc = 10 # number of frames that should contain the same person name to be added to the list

    # load training data and target labels , prepare for face detection
    def load_data(self):
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("Data/trainer.yml")
        with open("Data/labels.pickle", 'rb') as f:
            og_labels = pickle.load(f)
            self.labels = {v: k for k, v in og_labels.items()}
            self.face_cascade = cv2.CascadeClassifier("Data/haarcascade_frontalface_default.xml")

    def run(self):
        vid = cv2.VideoCapture(self.vid_name)
        count = 0
        while self.ret:
            ret, frame = vid.read()
            time.sleep(self.play_speed)
            # face detection block
            try:
                cvt_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                face = self.face_cascade.detectMultiScale(cvt_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                for (x, y, w, h) in face:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
                    capt_face = cvt_frame[y:y + h, x:x + w]
                    id_, precision = self.recognizer.predict(capt_face)
                    first = self.labels[id_]
                    precision = int(precision)
                    if 90 > precision > 60:
                        if first == self.labels[id_]:
                            count += 1
                            if count == self.fr_proc:
                                self.person.emit(self.labels[id_] + "                            " + str(precision)+"%")
                                count = 0
                        else:
                            count = 0
                    else:
                        pass
                resized = cv2.resize(frame, (491, 421), interpolation=cv2.INTER_AREA)
                height, width, channels = resized.shape
                if frame is None:
                    continue
                else:
                    # this block is for showing image in GUI
                    cvframe = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
                    image = QtGui.QImage(cvframe, width, height, width*3, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(image)
                    pixmapItem = QtWidgets.QGraphicsPixmapItem(pixmap)
                    self.frameItem.emit(pixmapItem)
            except cv2.error:
                print("votre video est apparament finie !")
                break


class Main(QtWidgets.QMainWindow, reconGUI.Ui_faceRecon):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.block = True
        self.scene = QtWidgets.QGraphicsScene(self)
        self.screen.setScene(self.scene)
        self.th = Thread()
        self.th.load_data()
        self.start.clicked.connect(self.playwebcam)
        self.block_signal.triggered.connect(self.blocksignal)
        self.th.frameItem.connect(self.scene.addItem)
        self.getVidSub.clicked.connect(self.playvid)
        self.horizontalSlider.valueChanged[int].connect(self.controlSpeed)
        self.th.person.connect(self.typename)

    def blocksignal(self):
        self.th.blockSignals(self.block)
        self.block = not self.block
        if not self.block:
            self.block_signal.setText("débloquer")
        else:
            self.block_signal.setText("bloquer")

    def playvid(self):
        self.controlSpeed()
        self.th.vid_name = os.path.basename(self.getVid.text()).strip()
        if not self.th.vid_name.find(".mp4") == len(self.th.vid_name) - 4:
            self.th.vid_name = self.th.vid_name + ".mp4"
        for (root, directories, files) in os.walk("../ressources/"):
            if self.th.vid_name in files:
                self.th.vid_name = "../ressources/" + self.th.vid_name
            else:
                QMessageBox.warning(self, 'video untrouvable !', "veuillez réessayer aver une autre nom", QMessageBox.Ok)
        self.getVid.clear()
        self.th.start()

    def playwebcam(self):
        self.th.vid_name = 0
        self.th.start()

    def controlSpeed(self):
        self.th.play_speed = self.horizontalSlider.value()/1000

    def typename(self, person_name):
        self.person_name.addItem(person_name)
        self.person_name.adjustSize()
        self.person_name.scrollToBottom()


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()


if __name__ == '__main__':

    main()
