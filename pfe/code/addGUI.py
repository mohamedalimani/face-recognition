# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reconGUI2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import reconGUI, os, time, cv2, sys


class addDataThread(QtCore.QThread):

    frameItem = QtCore.pyqtSignal(QtWidgets.QGraphicsPixmapItem)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.target_dir = "../target"
        self.target_name = ""
        self.path = ""
        self.lbp_classifier_face = 'lbpcascade_frontalface.xml'
        (self.im_width, self.im_height) = (110, 90)
        self.size = 1
        self.lbp_cascade_face = cv2.CascadeClassifier(f'Data/{self.lbp_classifier_face}')

    def run(self):
        self.camera = cv2.VideoCapture(0)
        global face_resize
        pin = sorted([int(n[:n.find('.')]) for n in os.listdir(self.path) if n[0] != '.'] + [0])[-1] + 1
        # The program loops until it has 40 face images .
        count = 0
        pause = 0
        t = 0
        count_max = 40
        while count < count_max:
            (working, frame) = self.camera.read()
            # Loop until the camera is working
            while not working:
                (working, frame) = self.camera.read()
                if not working:
                    print("Probleme avec la camera")
                    time.sleep(1)
                    t = t + 1
                    if t == 3:
                        print("probleme survenu le programme doit quitter !")
                        sys.exit(0)
            # Get image size
            height, width, channels = frame.shape
            # Flip frame
            frame = cv2.flip(frame, 1, 0)
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Detect faces
            faces = self.lbp_cascade_face.detectMultiScale(gray)
            # We only consider largest face
            faces = sorted(faces, key=lambda x: x[3])
            if faces:
                face_i = faces[0]
                (x, y, w, h) = [v * self.size for v in face_i]
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (self.im_width, self.im_height))
                # Draw rectangle and write name
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(frame, '%s - %d/40' % (self.target_name, count), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 0))
                # Remove false positives
                if w * 6 < width or h * 6 < height:
                    print("Non claire")
                else:
                    # To create diversity, only save every fith detected image
                    if pause == 0:
                        print("enregistrement de la capture " + str(count + 1) + "/" + str(count_max))

                        # Save image file
                        cv2.imwrite('%s/%s.png' % (self.path, pin), face_resize)
                        pin += 1
                        count += 1
                        pause = 1
            if pause > 0:
                pause = (pause + 1) % 3
                show_img = cv2.resize(frame, (571, 461), interpolation=cv2.INTER_AREA)
                height, width, channels = show_img.shape
                cvt_img = cv2.cvtColor(show_img, cv2.COLOR_BGR2RGB)
                saved_image = QtGui.QImage(cvt_img, width, height, width * 3, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(saved_image)
                pixmapItem = QtWidgets.QGraphicsPixmapItem(pixmap)
                self.frameItem.emit(pixmapItem)

        self.camera.release()
        cv2.destroyAllWindows()


class Ui_addnewface(object):
    def __init__(self):
        self.addDataThread = addDataThread()
        self.scene = QtWidgets.QGraphicsScene()

    def setupUi(self, addnewface):
        addnewface.setObjectName("addnewface")
        addnewface.resize(864, 600)
        self.centralwidget = QtWidgets.QWidget(addnewface)
        self.centralwidget.setObjectName("centralwidget")
        self.addDatascreen = QtWidgets.QGraphicsView(self.centralwidget)
        self.addDatascreen.setGeometry(QtCore.QRect(280, 10, 571, 461))
        self.addDatascreen.setObjectName("addDatascreen")
        self.addDataLabel = QtWidgets.QLineEdit(self.centralwidget)
        self.addDataLabel.setGeometry(QtCore.QRect(10, 70, 241, 51))
        self.addDataLabel.setObjectName("addDataLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 261, 41))
        font = QtGui.QFont()
        font.setFamily("padmaa")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.addDatastart = QtWidgets.QPushButton(self.centralwidget)
        self.addDatastart.setGeometry(QtCore.QRect(8, 140, 121, 31))
        self.addDatastart.setObjectName("addDatastart")
        addnewface.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(addnewface)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 864, 22))
        self.menubar.setObjectName("menubar")
        self.menunavigate = QtWidgets.QMenu(self.menubar)
        self.menunavigate.setObjectName("menunavigate")
        addnewface.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(addnewface)
        self.statusbar.setObjectName("statusbar")
        addnewface.setStatusBar(self.statusbar)
        self.toreconGUI = QtWidgets.QAction(addnewface)
        self.toreconGUI.setObjectName("toreconGUI")
        self.menunavigate.addAction(self.toreconGUI)
        self.menubar.addAction(self.menunavigate.menuAction())
        self.toreconGUI.triggered.connect(self.showWindow1)
        self.addDatascreen.setScene(self.scene)
        self.addDataThread.frameItem.connect(self.scene.addItem)

        self.retranslateUi(addnewface)
        QtCore.QMetaObject.connectSlotsByName(addnewface)

    def retranslateUi(self, addnewface):
        _translate = QtCore.QCoreApplication.translate
        addnewface.setWindowTitle(_translate("addnewface", "add Data"))
        self.label.setText(_translate("addnewface", "tapez le nom du personnage :"))
        self.addDatastart.setText(_translate("addnewface", "start"))
        self.menunavigate.setTitle(_translate("addnewface", "navigate"))
        self.toreconGUI.setText(_translate("addnewface", "vers reconnaissance facial"))
        self.toreconGUI.setStatusTip(_translate("addnewface", "ouvrir la page de réconnaissance faciale"))

    def showWindow1(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = reconGUI.Ui_faceRecon()
        self.ui.setupUi(self.window)
        self.window.show()

    def delay_start(self):
        time_passed = 6
        i = 0
        t1 = time.perf_counter()
        while i != time_passed:
            t2 = time.perf_counter()
            if t2 - t1 > i:
                i += 1
                print(time_passed - i)

    def add_data(self):
        msg = QtWidgets.QWidget()
        # create file and label it or find it if it already exists
        if len(self.addDataLabel.text()) == 0:
            QtWidgets.QMessageBox.warning(msg, 'entrée vide !', "nommer le person que vous voullez ajouter ", QtWidgets.QMessageBox.Ok)
        else:
            self.target_name = self.addDataLabel.text()
            self.addDataThread.target_name = self.target_name
            self.addDataThread.path = os.path.join(self.addDataThread.target_dir, self.target_name)
            if not os.path.isdir(self.addDataThread.path):
                os.mkdir(self.addDataThread.path)
            reponse = QtWidgets.QMessageBox.information(msg,'chronométre', "retarder l'operation par 5 seconds ?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if reponse == QtWidgets.QMessageBox.Yes:
                self.delay_start()
            elif reponse == QtWidgets.QMessageBox.No:
                pass

            self.addDataLabel.clear()
            self.addDataThread.start()


