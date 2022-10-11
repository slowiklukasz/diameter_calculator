from PyQt5.QtWidgets import QMessageBox, QComboBox, QLineEdit, QSpinBox, QCheckBox
from PyQt5.QtCore import QVariant

from qgis.core import QgsVectorLayer, QgsField
from qgis.gui import QgsFileWidget

import time
import math


class CirDiamCalc:
    
    def cir_to_diam(lyr, cir_col_nm, diam_col_nm, sep_type, rounding, chk_codice):
        start = time.time()
        
        lyr.startEditing()
        
        # WYSZUKANIE KOLUMNY Z OBWODAMI, ZDEFINIOWANIE KOLUMNY Z ŚREDNICAMI
        flds = lyr.fields()
        cir_ind = flds.indexOf(cir_col_nm)
        cir_fld = flds.field(cir_ind)
        diam_fld = QgsField(f"{diam_col_nm}", QVariant.String, len=cir_fld.length())
        
        # SPRAWDZENIE CZY WARSTWA ZWAWIERA ODPOWIEDNIĄ KOLUMNĘ/STWORZENIE NOWEJ KOLUMNY
        idx = lyr.fields().indexOf(diam_fld.name())

        if idx == -1:
            lyr.dataProvider().addAttributes([diam_fld])
            lyr.updateFields()

        # PRZELICZENIE ŚREDNICY ORAZ DOPISANIE GO DO NOWEJ KOLUMNY
        ftrs = lyr.getFeatures()
        for ftr in ftrs:
            cir = ftr[cir_fld.name()]
            codice = ftr["codice"] if chk_codice else 'P103108'
            
            d = ""
            if codice in ('P103108', 'P103118') and cir:
                if sep_type in cir:
                    for i in str(cir).split(sep_type):
                        if i != "": # when last char is ";"
                            tmp =   round(float(i)/ math.pi, rounding) if rounding>0 else \
                                    round(float(i)/ math.pi)
                            d += "{};".format(tmp)
                            ftr[diam_fld.name()] = d[:-1]
                else:
                    ftr[diam_fld.name()] =  str(round(float(cir)/math.pi, rounding)) \
                                            if rounding>0 else \
                                            str(round(float(cir)/math.pi))
                lyr.updateFeature(ftr)
        lyr.commitChanges()

        stop = time.time()
 
        msg = f"Zakończono! \n\n\
        - Dane z pola '{cir_col_nm}' zostały przeliczone na średnice i dodane do kolumny '{diam_col_nm}'.\n\
        - Czas wykonania obliczeń: {round(stop - start)} sek."

        return msg
        
        
    def diam_to_cir(lyr, diam_col_nm, cir_col_nm, sep_type, rounding, chk_codice):
        start = time.time()
        
        lyr.startEditing()
        
        # WYSZUKANIE KOLUMNY Z ŚREDNICAMI, ZDEFINIOWANIE KOLUMNY Z OBWODAMI
        flds = lyr.fields()
        diam_ind = flds.indexOf(diam_col_nm)
        diam_fld = flds.field(diam_ind)
        cir_fld = QgsField(f"{cir_col_nm}", QVariant.String, len=diam_fld.length())
        
        # SPRAWDZENIE CZY WARSTWA ZWAWIERA ODPOWIEDNIĄ KOLUMNĘ/STWORZENIE NOWEJ KOLUMNY
        idx = lyr.fields().indexOf(cir_fld.name())

        if idx == -1:
            lyr.dataProvider().addAttributes([cir_fld])
            lyr.updateFields()

        # PRZELICZENIE OBWODU ORAZ DOPISANIE GO DO NOWEJ KOLUMNY
        ftrs = lyr.getFeatures()
        for ftr in ftrs:
            diam = ftr[diam_fld.name()]
            codice = ftr["codice"] if chk_codice else 'P103108'
            
            c = ""
            if codice in ('P103108', 'P103118') and diam:
                if sep_type in diam:
                    for i in str(diam).split(sep_type):
                        if i != "": # when last char is ";"
                            tmp =   round(float(i) * math.pi, rounding) if rounding>0 else \
                                    round(float(i) * math.pi)
                            c += "{};".format(tmp)
                            ftr[cir_fld.name()] = c[:-1]
                else:
                    ftr[cir_fld.name()] =   str(round(float(diam) * math.pi, rounding)) \
                                            if rounding>0 else \
                                            str(round(float(diam) * math.pi))
                    
                lyr.updateFeature(ftr)
        lyr.commitChanges()

        stop = time.time()
 
        msg = f"Zakończono! \n\n\
        - Dane z pola '{diam_col_nm}' zostały przeliczone na obwody i dodane do kolumny '{cir_col_nm}'.\n\
        - Czas wykonania obliczeń: {round(stop - start)} sek."

        return msg
        
        
#    def reset_widgets(idx, *args):
#        for arg in args:
#            if isinstance(arg, QgsFileWidget):
#                arg.setFilePath("")
#            elif isinstance(arg, QLineEdit):
#                arg.setText("obw") if idx==1 else arg.setText("sred") # error with 0 idx here
#            elif isinstance(arg, QComboBox) and arg.count()>0:
#                arg.setCurrentIndex(0)
#            elif isinstance(arg, QSpinBox):
#                arg.setValue(0)
#            elif isinstance(arg, QCheckBox):
#                arg.setChecked(True)