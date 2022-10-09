from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QVariant

from qgis.core import QgsVectorLayer, QgsField

import time
import math


class CirDiamCalc:
    
    def cir_to_diam(lyr, cir_col_nm, diam_col_nm, sep_type, rounding):
        start = time.time()
        
        lyr.startEditing()
        
        # WYSZUKANIE KOLUMNY Z OBWODAMI, ZDEFINIOWANIE KOLUMNY Z ŚREDNICAMI
        flds = lyr.fields()
        obw_ind = flds.indexOf(cir_col_nm)
        obw_fld = flds.field(obw_ind)
        d_fld = QgsField(f"{diam_col_nm}", QVariant.String, len=obw_fld.length())
        
        # SPRAWDZENIE CZY WARSTWA ZWAWIERA ODPOWIEDNIĄ KOLUMNĘ/STWORZENIE NOWEJ KOLUMNY
        idx = lyr.fields().indexOf(d_fld.name())

        if idx == -1:
            lyr.dataProvider().addAttributes([d_fld])
            lyr.updateFields()

        # PRZELICZENIE ŚREDNICY ORAZ DOPISANIE GO DO NOWEJ KOLUMNY
        ftrs = lyr.getFeatures()
        for ftr in ftrs:
            obw = ftr[obw_fld.name()]
            codice = ftr["codice"]
            
            d = ""
            if codice in ('P103108', 'P103118') and obw:
                if sep_type in obw:
                    for i in str(obw).split(sep_type):
                        if i != "": # when last char is ";"
                            tmp = round(float(i)/ math.pi)
                            d += "{};".format(tmp)
                            ftr[d_fld.name()] = d[:-1]
                else:
                    ftr[d_fld.name()] = str(round(float(obw)/math.pi, rounding))
                    
                lyr.updateFeature(ftr)
        lyr.commitChanges()

        stop = time.time()
 
        msg = f"Zakończono! \n\n\
        - Dane z pola '{cir_col_nm}' zostały przeliczone na średnice i dodane do kolumny '{diam_col_nm}'.\n\
        - Czas wykonania obliczeń: {round(stop - start)} sek."

        return msg

if __name__ == "__console__":
    fn = r"C:\Users\lukas\Desktop\CHM, GEOBIA\WALIDATOR-DANE\BLEDNE\P1.shp"
    lyr = QgsVectorLayer(fn, "P1", "ogr")

    cir_col_nm = "diam_tronc"
    diam_col_nm = "sredn_tst"
    sep_type = ";"
    
    cir_to_diam(lyr, cir_col_nm, diam_col_nm, sep_type)