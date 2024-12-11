


from PyQt5 import QtCore, QtGui, QtWidgets

from SDDImage import Ui_SDDImage
from SDDVideo   import Ui_SDDVideo
class Ui_AdminHome(object):

    def detect_Image(self):
        try:
            self.res = QtWidgets.QDialog()
            self.ui = Ui_SDDImage()
            self.ui.setupUi(self.res)
            self.res.show()

        except Exception as e:
            print("Error=" + e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)
            print(e)

    def detect_video(self):
        try:
            self.res = QtWidgets.QDialog()
            self.ui = Ui_SDDVideo()
            self.ui.setupUi(self.res)
            self.res.show()

        except Exception as e:
            print("Error=" + e.args[0])
            tb = sys.exc_info()[2]
            print(tb.tb_lineno)
            print(e)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(664, 599)
        Dialog.setStyleSheet("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, -30, 681, 631))
        self.label.setStyleSheet("background-image: url(../SocialDistance/images/sd3.jpg);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 190, 341, 41))
        self.pushButton.setStyleSheet("font: 14pt \"Georgia\";\n"
"background-color: rgb(0, 85, 127);\n"
"color: rgb(225,225,225);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.detect_Image)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 310, 341, 41))
        self.pushButton_2.setStyleSheet("\n"
"font: 14pt \"Georgia\";\n"
"background-color: rgb(0, 85, 127);\n"
"color: rgb(225,225,225);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.detect_video)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AdminHome"))
        self.pushButton.setText(_translate("Dialog", "Social Distance Detection with Image"))
        self.pushButton_2.setText(_translate("Dialog", "Social Distance Detection with Video"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
