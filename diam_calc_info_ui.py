# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'diam_calc_dialog_info.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_InfoDlg(object):
    def setupUi(self, InfoDlg):
        InfoDlg.setObjectName("InfoDlg")
        InfoDlg.resize(603, 187)
        self.info_ted = QtWidgets.QTextEdit(InfoDlg)
        self.info_ted.setGeometry(QtCore.QRect(20, 10, 571, 161))
        self.info_ted.setReadOnly(True)
        self.info_ted.setObjectName("info_ted")

        self.retranslateUi(InfoDlg)
        QtCore.QMetaObject.connectSlotsByName(InfoDlg)

    def retranslateUi(self, InfoDlg):
        _translate = QtCore.QCoreApplication.translate
        InfoDlg.setWindowTitle(_translate("InfoDlg", "Info"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    InfoDlg = QtWidgets.QDialog()
    ui = Ui_InfoDlg()
    ui.setupUi(InfoDlg)
    InfoDlg.show()
    sys.exit(app.exec_())
