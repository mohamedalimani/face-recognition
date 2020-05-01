# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'reconGUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import addGUI, cv2, time, pickle,os
from datetime import datetime


class ReconThread(QtCore.QThread):
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


class Ui_faceRecon(object):
    def __init__(self):
        self.reconThread = ReconThread()
        self.scene = QtWidgets.QGraphicsScene()
        self.vidname = "webcam"
        self.msg = QtWidgets.QMessageBox()

    def setupUi(self, faceRecon):
        faceRecon.setObjectName("faceRecon")
        faceRecon.resize(864, 600)
        self.centralwidget = QtWidgets.QWidget(faceRecon)
        self.centralwidget.setObjectName("centralwidget")
        self.getVidSub = QtWidgets.QPushButton(self.centralwidget)
        self.getVidSub.setGeometry(QtCore.QRect(30, 120, 89, 25))
        self.getVidSub.setObjectName("getVidSub")
        self.getVidlabel = QtWidgets.QLabel(self.centralwidget)
        self.getVidlabel.setGeometry(QtCore.QRect(30, 30, 231, 17))
        self.getVidlabel.setObjectName("getVidlabel")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(30, 170, 181, 71))
        self.start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("webcam.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.start.setIcon(icon)
        self.start.setIconSize(QtCore.QSize(41, 49))
        self.start.setObjectName("start")
        self.getVid = QtWidgets.QLineEdit(self.centralwidget)
        self.getVid.setGeometry(QtCore.QRect(30, 60, 231, 51))
        self.getVid.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.getVid.setObjectName("getVid")
        self.screen = QtWidgets.QGraphicsView(self.centralwidget)
        self.screen.setGeometry(QtCore.QRect(290, 10, 491, 421))
        self.screen.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.screen.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.screen.setObjectName("screen")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 310, 160, 16))
        self.horizontalSlider.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.horizontalSlider.setMinimum(5)
        self.horizontalSlider.setMaximum(25)
        self.horizontalSlider.setSliderPosition(15)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setInvertedAppearance(True)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.QsliderLabel = QtWidgets.QLabel(self.centralwidget)
        self.QsliderLabel.setGeometry(QtCore.QRect(30, 270, 171, 17))
        self.QsliderLabel.setObjectName("QsliderLabel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 296, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.personLabel = QtWidgets.QLabel(self.centralwidget)
        self.personLabel.setGeometry(QtCore.QRect(30, 340, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.personLabel.setFont(font)
        self.personLabel.setObjectName("personLabel")
        self.person_name = QtWidgets.QListWidget(self.centralwidget)
        self.person_name.setGeometry(QtCore.QRect(30, 380, 221, 101))
        self.person_name.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.person_name.setSelectionRectVisible(True)
        self.person_name.setObjectName("person_name")
        faceRecon.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(faceRecon)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 864, 22))
        self.menubar.setObjectName("menubar")
        self.menumenu = QtWidgets.QMenu(self.menubar)
        self.menumenu.setObjectName("menumenu")
        self.menunavigate = QtWidgets.QMenu(self.menubar)
        self.menunavigate.setObjectName("menunavigate")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        faceRecon.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(faceRecon)
        self.statusbar.setObjectName("statusbar")
        faceRecon.setStatusBar(self.statusbar)
        self.block_signal = QtWidgets.QAction(faceRecon)
        self.block_signal.setObjectName("block_signal")
        self.exitProg = QtWidgets.QAction(faceRecon)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("stop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitProg.setIcon(icon1)
        self.exitProg.setObjectName("exitProg")
        self.toAddtarget = QtWidgets.QAction(faceRecon)
        self.toAddtarget.setObjectName("toAddtarget")
        self.actionsauvegarder = QtWidgets.QAction(faceRecon)
        self.actionsauvegarder.setObjectName("actionsauvegarder")
        self.actioncomment_ca_marche = QtWidgets.QAction(faceRecon)
        self.actioncomment_ca_marche.setObjectName("actioncomment_ca_marche")
        self.menumenu.addAction(self.block_signal)
        self.menumenu.addAction(self.exitProg)
        self.menumenu.addAction(self.actionsauvegarder)
        self.menunavigate.addAction(self.toAddtarget)
        self.menuhelp.addAction(self.actioncomment_ca_marche)
        self.menubar.addAction(self.menumenu.menuAction())
        self.menubar.addAction(self.menunavigate.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())
        self.toAddtarget.triggered.connect(self.showWindow2)
        self.actionsauvegarder.triggered.connect(self.save_labels)
        self.actioncomment_ca_marche.triggered.connect(self.help)

        self.retranslateUi(faceRecon)
        QtCore.QMetaObject.connectSlotsByName(faceRecon)

    def retranslateUi(self, faceRecon):
        _translate = QtCore.QCoreApplication.translate
        faceRecon.setWindowTitle(_translate("faceRecon", "face recognition"))
        self.getVidSub.setText(_translate("faceRecon", "soumettre"))
        self.getVidSub.setShortcut(_translate("faceRecon", "Return"))
        self.getVidlabel.setText(_translate("faceRecon", "déposez une vidéo ici (.mp4)"))
        self.start.setStatusTip(_translate("faceRecon", "cliquez ici si vous voulez utiliser le webcam (ctrl+w)"))
        self.start.setText(_translate("faceRecon", "  utiliser webcam"))
        self.start.setShortcut(_translate("faceRecon", "Ctrl+W"))
        self.screen.setStatusTip(_translate("faceRecon", "votre video va etre afficher dans cette écran "))
        self.horizontalSlider.setStatusTip(_translate("faceRecon", "controller la vitesse du traitement du video"))
        self.QsliderLabel.setStatusTip(_translate("faceRecon", "controller la vitesse du traitement du video"))
        self.QsliderLabel.setText(_translate("faceRecon", "vitesse de lecture"))
        self.label.setText(_translate("faceRecon", "x2"))
        self.personLabel.setText(_translate("faceRecon", "nom                 précision"))
        self.person_name.setStatusTip(_translate("faceRecon", "liste des visages réconnue"))
        self.menumenu.setTitle(_translate("faceRecon", "option"))
        self.menunavigate.setTitle(_translate("faceRecon", "navigate"))
        self.menuhelp.setTitle(_translate("faceRecon", "help"))
        self.block_signal.setText(_translate("faceRecon", "bloquer l\'ecran "))
        self.block_signal.setStatusTip(_translate("faceRecon", "bloquer tous les signaux vennant du thread (ctrl+B)"))
        self.block_signal.setShortcut(_translate("faceRecon", "Ctrl+B"))
        self.exitProg.setText(_translate("faceRecon", "arrêt forcé"))
        self.exitProg.setStatusTip(_translate("faceRecon", "arret forcé et sortir du programme (ctrl+E)"))
        self.exitProg.setShortcut(_translate("faceRecon", "Ctrl+E"))
        self.toAddtarget.setText(_translate("faceRecon", "ajouter data"))
        self.toAddtarget.setStatusTip(_translate("faceRecon", "ajouter un nouveau dossier contenant des images des personnages"))
        self.actionsauvegarder.setText(_translate("faceRecon", "sauvegarder "))
        self.actionsauvegarder.setStatusTip(_translate("faceRecon", "sauvegarder la listes des persons reconnues"))
        self.actionsauvegarder.setShortcut(_translate("faceRecon", "Ctrl+S"))
        self.actioncomment_ca_marche.setText(_translate("faceRecon", "lire la suite ?"))

    def showWindow2(self):
        self.adDaTh = addGUI.AddDataThread()
        self.window = QtWidgets.QMainWindow()
        self.ui = addGUI.Ui_Addnewface()
        self.ui.setupUi(self.window)
        self.ui.addDatastart.clicked.connect(self.ui.add_data)
        self.window.show()

    def save_labels(self):
        if self.person_name.count() != 0:
            labels = [self.person_name.item(i).text() for i in range(len(self.person_name))]
            with open("labels.txt", 'a') as f:
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                f.write(f"\n \n# video name : {os.path.basename(self.vidname)} # date : {dt_string} \n \n")
                for label in labels:
                    f.write("-"+label + "\n")
                f.write("\n \n")
        else:
            QtWidgets.QMessageBox.question(QtWidgets.QWidget(), "liste vide", " l'AI n'a reconnu aucunne personne !", self.msg.Ok)

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
        self.vidname = self.getVid.text().strip()
        if not self.reconThread.vid_name.find(".mp4") == len(self.reconThread.vid_name) - 4:
            self.reconThread.vid_name = self.reconThread.vid_name + ".mp4"
        for (root, directories, files) in os.walk("../ressources/"):
            if self.reconThread.vid_name in files:
                self.reconThread.vid_name = "../ressources/" + self.reconThread.vid_name
            else:
                QtWidgets.QMessageBox.warning(QtWidgets.QWidget(), 'video untrouvable !', "veuillez réessayer aver une autre nom", self.msg.Ok)
        self.getVid.clear()
        self.person_name.clear()
        self.reconThread.start()

    def playwebcam(self):
        self.reconThread.vid_name = 0
        self.person_name.clear()
        self.reconThread.start()

    def controlSpeed(self):
        self.reconThread.play_speed = self.horizontalSlider.value() / 1000

    def typename(self, person_name):
        self.person_name.addItem(person_name)
        self.person_name.adjustSize()
        self.person_name.scrollToBottom()

    def force_exit(self):
        is_exit = QtWidgets.QMessageBox.warning(QtWidgets.QWidget(), "attention !", "étes vous sure d'arreter le programme !",self.msg.Yes | self.msg.No, self.msg.No)
        if is_exit == self.msg.Yes:
            exit()
        elif is_exit == self.msg.No:
            pass

    def help(self):
        QtWidgets.QMessageBox.information(QtWidgets.QWidget(), "comment ca marche ?", "cette application est un systemme de réconnaissance faciale", self.msg.Ok)
