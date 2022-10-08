from qgis.PyQt.QtWidgets import *
from .diam_calc_info_ui import Ui_InfoDlg


class DlgInfo(QDialog, Ui_InfoDlg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)