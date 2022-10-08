from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QVariant

from qgis.utils import iface
from qgis.core import QgsVectorLayer, QgsField

import time
import math


class DiamCalculator:
    
    def obw_d_calc(lyr, obw_col_nm, d_col_nm, sep_type):
        start = time.time()
        
        lyr.startEditing()
        
        # WYSZUKANIE KOLUMNY Z OBWODAMI, ZDEFINIOWANIE KOLUMNY Z ŚREDNICAMI
        flds = lyr.fields()
        obw_ind = flds.indexOf(obw_col_nm)
        obw_fld = flds.field(obw_ind)
        d_fld = QgsField(f"{d_col_nm}", QVariant.String, len=obw_fld.length())
        
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
                    for i in obw.split(sep_type):
                        if i != "": # when last char is ";"
                            tmp = round(float(i)/ math.pi)
                            d += "{};".format(tmp)
                            ftr[d_fld.name()] = d[:-1]
                else:
                    ftr[d_fld.name()] = str(round(float(obw)/math.pi))
                    
                lyr.updateFeature(ftr)
        lyr.commitChanges()

        stop = time.time()
        iface.addVectorLayer(lyr.dataProvider().dataSourceUri(), \
                            lyr.sourceName(), \
                            "ogr")
 
        msg = f"Zakończono! \n\n\
        - Dane z pola '{obw_col_nm}' zostały przeliczone na średnice i dodane do kolumny '{d_col_nm}'.\n\
        - Czas wykonania obliczeń: {round(stop - start)} sek."

        return msg

if __name__ == "__console__":
    fn = r"C:\Users\lukas\Desktop\CHM, GEOBIA\WALIDATOR-DANE\BLEDNE\P1.shp"
    lyr = QgsVectorLayer(fn, "P1", "ogr")

    obw_col_nm = "diam_tronc"
    d_col_nm = "sredn_tst"
    sep_type = ";"
    
    obw_d_calc(lyr, obw_col_nm, d_col_nm, sep_type)