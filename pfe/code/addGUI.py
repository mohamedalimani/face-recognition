from PyQt5 import QtCore, QtGui, QtWidgets
import reconGUI, os, time, cv2, sys, pickle
from PIL import Image
import numpy as np
import shutil


class AddDataThread(QtCore.QThread):

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
        self.count_max = 40

    def run(self):
        self.camera = cv2.VideoCapture(0)
        global face_resize
        pin = sorted([int(n[:n.find('.')]) for n in os.listdir(self.path) if n[0] != '.'] + [0])[-1] + 1
        # The program loops until it has 40 face images .
        count = 0
        pause = 0
        t = 0
        # count_max = 40
        while count < self.count_max:
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
                cv2.putText(frame, '%s - %d/%d' % (self.target_name, count, self.count_max), (x - 10, y - 10), cv2.FONT_HERSHEY_PLAIN,1, (0, 255, 0))
                # Remove false positives
                if w * 6 < width or h * 6 < height:
                    print("Non claire")
                else:
                    # To create diversity, only save every fith detected image
                    if pause == 0:
                        print("enregistrement de la capture " + str(count + 1) + "/" + str(self.count_max))

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


class Ui_Addnewface(object):
    def __init__(self):
        self.addDataThread = AddDataThread()
        self.scene = QtWidgets.QGraphicsScene()

    def setupUi(self, addnewface):
        addnewface.setObjectName("addnewface")
        addnewface.resize(863, 600)
        self.centralwidget = QtWidgets.QWidget(addnewface)
        self.centralwidget.setObjectName("centralwidget")
        self.addDatascreen = QtWidgets.QGraphicsView(self.centralwidget)
        self.addDatascreen.setGeometry(QtCore.QRect(280, 10, 571, 461))
        self.addDatascreen.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.addDatascreen.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.addDatascreen.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.addDatascreen.setObjectName("addDatascreen")
        self.addDataLabel = QtWidgets.QLineEdit(self.centralwidget)
        self.addDataLabel.setGeometry(QtCore.QRect(10, 70, 241, 51))
        self.addDataLabel.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
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
        font = QtGui.QFont()
        font.setFamily("URW Bookman L")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.addDatastart.setFont(font)
        self.addDatastart.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addDatastart.setIcon(icon)
        self.addDatastart.setIconSize(QtCore.QSize(52, 26))
        self.addDatastart.setObjectName("addDatastart")
        self.imagesNumber = QtWidgets.QSlider(self.centralwidget)
        self.imagesNumber.setGeometry(QtCore.QRect(10, 230, 201, 16))
        self.imagesNumber.setMinimum(10)
        self.imagesNumber.setMaximum(100)
        self.imagesNumber.setSingleStep(10)
        self.imagesNumber.setSliderPosition(40)
        self.imagesNumber.setOrientation(QtCore.Qt.Horizontal)
        self.imagesNumber.setObjectName("imagesNumber")
        self.imgNumLabel = QtWidgets.QLabel(self.centralwidget)
        self.imgNumLabel.setGeometry(QtCore.QRect(10, 190, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.imgNumLabel.setFont(font)
        self.imgNumLabel.setObjectName("imgNumLabel")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(70, 250, 31, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(180, 250, 41, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 290, 141, 17))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.train_faces_btn = QtWidgets.QPushButton(self.centralwidget)
        self.train_faces_btn.setGeometry(QtCore.QRect(10, 330, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Ubuntu Condensed")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.train_faces_btn.setFont(font)
        self.train_faces_btn.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.train_faces_btn.setIcon(icon1)
        self.train_faces_btn.setIconSize(QtCore.QSize(29, 30))
        self.train_faces_btn.setObjectName("train_faces_btn")
        self.deletlabel = QtWidgets.QLabel(self.centralwidget)
        self.deletlabel.setGeometry(QtCore.QRect(10, 400, 211, 21))
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(13)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.deletlabel.setFont(font)
        self.deletlabel.setObjectName("deletlabel")
        self.deletebtn = QtWidgets.QPushButton(self.centralwidget)
        self.deletebtn.setGeometry(QtCore.QRect(10, 500, 121, 31))
        font = QtGui.QFont()
        font.setFamily("URW Bookman L")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.deletebtn.setFont(font)
        self.deletebtn.setObjectName("deletebtn")
        self.addDataLabel_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.addDataLabel_2.setGeometry(QtCore.QRect(10, 430, 241, 51))
        self.addDataLabel_2.setCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        self.addDataLabel_2.setObjectName("addDataLabel_2")
        addnewface.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(addnewface)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 863, 22))
        self.menubar.setObjectName("menubar")
        self.menunavigate = QtWidgets.QMenu(self.menubar)
        self.menunavigate.setObjectName("menunavigate")
        self.menuoption = QtWidgets.QMenu(self.menubar)
        self.menuoption.setObjectName("menuoption")
        addnewface.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(addnewface)
        self.statusbar.setObjectName("statusbar")
        addnewface.setStatusBar(self.statusbar)
        self.toreconGUI = QtWidgets.QAction(addnewface)
        self.toreconGUI.setObjectName("toreconGUI")
        self.actionarret_forc = QtWidgets.QAction(addnewface)
        self.actionarret_forc.setObjectName("actionarret_forc")
        self.actionsupprimer_un_repertoire = QtWidgets.QAction(addnewface)
        self.actionsupprimer_un_repertoire.setObjectName("actionsupprimer_un_repertoire")
        self.menunavigate.addAction(self.toreconGUI)
        self.menuoption.addAction(self.actionarret_forc)
        self.menubar.addAction(self.menunavigate.menuAction())
        self.menubar.addAction(self.menuoption.menuAction())
        self.toreconGUI.triggered.connect(self.showWindow1)
        self.addDatascreen.setScene(self.scene)
        self.addDataThread.frameItem.connect(self.scene.addItem)
        self.actionarret_forc.triggered.connect(self.force_exit2)
        self.train_faces_btn.clicked.connect(self.train_data)
        self.deletebtn.clicked.connect(self.delete_label)

        self.retranslateUi(addnewface)
        QtCore.QMetaObject.connectSlotsByName(addnewface)

    def retranslateUi(self, addnewface):
        _translate = QtCore.QCoreApplication.translate
        addnewface.setWindowTitle(_translate("addnewface", "add Data"))
        self.addDatascreen.setStatusTip(_translate("addnewface", "déplacer votre tete au milieu de l\'ecran"))
        self.label.setText(_translate("addnewface", "tapez le nom du personnage :"))
        self.addDatastart.setStatusTip(_translate("addnewface", "ajouter des photo au base de donnée"))
        self.addDatastart.setText(_translate("addnewface", "  start"))
        self.addDatastart.setShortcut(_translate("addnewface", "Return"))
        self.imagesNumber.setStatusTip(_translate("addnewface", "choisir le nombre des images "))
        self.imgNumLabel.setText(_translate("addnewface", "nombre des photo"))
        self.label_3.setText(_translate("addnewface", "x40"))
        self.label_4.setText(_translate("addnewface", "x100"))
        self.label_5.setText(_translate("addnewface", "entrainer l\'AI :"))
        self.train_faces_btn.setStatusTip(_translate("addnewface", "entrainer l\'AI a reconnaiser les personnes que tu as ajouté"))
        self.train_faces_btn.setText(_translate("addnewface", "    entraine"))
        self.deletlabel.setText(_translate("addnewface", "supprimer un reportoire :"))
        self.deletebtn.setText(_translate("addnewface", "supprimer"))
        self.menunavigate.setTitle(_translate("addnewface", "navigate"))
        self.menuoption.setTitle(_translate("addnewface", "option"))
        self.toreconGUI.setText(_translate("addnewface", "vers reconnaissance facial"))
        self.toreconGUI.setStatusTip(_translate("addnewface", "ouvrir la page de réconnaissance faciale"))
        self.actionarret_forc.setText(_translate("addnewface", "arret forcé (ctrl+E)"))
        self.actionarret_forc.setShortcut(_translate("addnewface", "Ctrl+E"))
        self.actionsupprimer_un_repertoire.setText(_translate("addnewface", "supprimer un repertoire"))

    def showWindow1(self):
        self.reconThread = reconGUI.ReconThread()
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
        self.scene.clear()
        self.addDataThread.count_max = self.imagesNumber.value()
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

    def force_exit2(self):
        msg = QtWidgets.QMessageBox()
        is_exit = msg.warning(QtWidgets.QWidget(), "attention !", "étes vous sure d'arreter le programme !", msg.Yes | msg.No, msg.No)
        if is_exit == msg.Yes:
            exit()
        elif is_exit == msg.No:
            pass

    def train_data(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_dir = os.path.join(BASE_DIR, "../target/")
        face_cascade = cv2.CascadeClassifier("Data/haarcascade_frontalface_default.xml")
        recognizer = cv2.face.LBPHFaceRecognizer_create()

        current_id = 0
        label_ids = {}
        y_labels = []
        x_train = []

        for root, dirs, files in os.walk(image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    path = os.path.join(root, file)
                    label = os.path.basename(os.path.dirname(path)).replace(' ', '-').lower()
                    if not label in label_ids:
                        label_ids[label] = current_id
                        current_id += 1
                    id_ = label_ids[label]
                    pil_image = Image.open(path).convert("L")  # convert image into gray
                    size = (550, 550)
                    final_image = pil_image.resize(size, Image.ANTIALIAS)
                    image_array = np.array(final_image, "uint8")
                    faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.1, minNeighbors=5,
                                                          minSize=(30, 30))
                    for (x, y, w, h) in faces:
                        roi = image_array[y:y + h, x:x + w]
                        x_train.append(roi)
                        y_labels.append(id_)

        with open("Data/labels.pickle", 'wb') as f:
            pickle.dump(label_ids, f)

        recognizer.train(x_train, np.array(y_labels))
        recognizer.save("Data/trainer.yml")
        msg = QtWidgets.QMessageBox()
        msg.information(QtWidgets.QWidget(), "success !", "l'entrainement est terminé avec succées", msg.Ok)

    def delete_label(self):
        y = self.addDataLabel_2.text().strip()
        dellabel = os.path.basename(y)
        msg = QtWidgets.QMessageBox()
        x = QtWidgets.QMessageBox.warning(QtWidgets.QWidget(),"WARNING !!!", f"voullez vous vraiment supprimer le repertoire sous le nom {dellabel}", msg.No | msg.Yes, msg.No)
        if x == QtWidgets.QMessageBox.Yes:
            dirlist = os.listdir(path="../target/")
            if dellabel in dirlist:
                shutil.rmtree(os.path.join("../target/", dellabel))
                QtWidgets.QMessageBox.information(QtWidgets.QWidget(), "succees !", f"le repertoire {dellabel} ", msg.Ok)
            else:
                QtWidgets.QMessageBox.question(QtWidgets.QWidget(), "repertoire non trouvé !", "verifiez le nom du répertoire ",msg.Ok)
        elif x == QtWidgets.QMessageBox.No:
            pass
        self.addDataLabel_2.clear()
