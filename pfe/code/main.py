from PyQt5 import QtWidgets
import reconGUI, addGUI


class Main(QtWidgets.QMainWindow, reconGUI.Ui_faceRecon, addGUI.Ui_Addnewface):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.setupUi(self)
        self.reconThread = reconGUI.ReconThread()
        self.block = True
        self.scene = QtWidgets.QGraphicsScene(self)
        self.screen.setScene(self.scene)
        self.reconThread.load_data()
        self.start.clicked.connect(self.playwebcam)
        self.block_signal.triggered.connect(self.blocksignal)
        self.reconThread.frameItem.connect(self.scene.addItem)
        self.getVidSub.clicked.connect(self.playvid)
        self.horizontalSlider.valueChanged[int].connect(self.controlSpeed)
        self.reconThread.person.connect(self.typename)
        self.exitProg.triggered.connect(self.force_exit)


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec_()


if __name__ == '__main__':

    main()
