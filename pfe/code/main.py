from PyQt5 import QtCore, QtGui, QtWidgets
import cv2, time, os, pickle, reconGUI, addGUI
from PyQt5.QtWidgets import QMessageBox


class reconThread(QtCore.QThread):
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
                                self.person.emit(
                                    self.labels[id_] + "                            " + str(precision) + "%")
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
                    image = QtGui.QImage(cvframe, width, height, width * 3, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(image)
                    pixmapItem = QtWidgets.QGraphicsPixmapItem(pixmap)
                    self.frameItem.emit(pixmapItem)
            except cv2.error:
                print("votre video est apparament finie !")
                break


class Main(QtWidgets.QMainWindow, reconGUI.Ui_faceRecon, addGUI.Ui_addnewface):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.block = True
        self.scene = QtWidgets.QGraphicsScene(self)
        self.screen.setScene(self.scene)
        self.reconThread = reconThread()
        self.reconThread.load_data()
        self.start.clicked.connect(self.playwebcam)
        self.block_signal.triggered.connect(self.blocksignal)
        self.reconThread.frameItem.connect(self.scene.addItem)
        self.getVidSub.clicked.connect(self.playvid)
        self.horizontalSlider.valueChanged[int].connect(self.controlSpeed)
        self.reconThread.person.connect(self.typename)
        self.exitProg.triggered.connect(self.force_exit)

    def blocksignal(self):
        self.reconThread.blockSignals(self.block)
        self.block = not self.block
        if not self.block:
            self.block_signal.setText("débloquer")
        else:
            self.block_signal.setText("bloquer")

    def playvid(self):
        self.controlSpeed()
        self.reconThread.vid_name = os.path.basename(self.getVid.text()).strip()
        if not self.reconThread.vid_name.find(".mp4") == len(self.reconThread.vid_name) - 4:
            self.reconThread.vid_name = self.reconThread.vid_name + ".mp4"
        for (root, directories, files) in os.walk("../ressources/"):
            if self.reconThread.vid_name in files:
                self.reconThread.vid_name = "../ressources/" + self.reconThread.vid_name
            else:
                QMessageBox.warning(self, 'video untrouvable !', "veuillez réessayer aver une autre nom", QMessageBox.Ok)
        self.getVid.clear()
        self.reconThread.start()

    def playwebcam(self):
        self.reconThread.vid_name = 0
        self.reconThread.start()

    def controlSpeed(self):
        self.reconThread.play_speed = self.horizontalSlider.value() / 1000

    def typename(self, person_name):
        self.person_name.addItem(person_name)
        self.person_name.adjustSize()
        self.person_name.scrollToBottom()

    def force_exit(self):
        is_exit = QMessageBox.warning(self, "attention !", "étes vous sure d'arreter le programme !", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if is_exit == QMessageBox.Yes:
            exit()
        elif is_exit == QMessageBox.No:
            pass


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()


if __name__ == '__main__':

    main()
