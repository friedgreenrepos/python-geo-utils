import sys
import xmltodict
import csv
import geoutils
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QDesktopWidget,
    QLineEdit,
    QGridLayout,
    QFileDialog,
    QErrorMessage,
    QLabel)
from PyQt5.QtCore import QDir, pyqtSlot
from PyQt5.QtGui import QIcon
from itertools import combinations

info_labels = {
    'match_distance': {
        'en': "Return a list of same-distance points couples from a file of 2D points",
        'it': "Passare in input un file TXT/CSV con le coordinate dei punti.\nIn output si ottiene il file TXT con le coppie di punti che hanno la stessa distanza."
    },
    'xml_filler': {
        'en': "Update an xml file with the points given as input",
        'it': "Passare come primo input il file XML, poi il file TXT/CSV dei punti.\nIn output si ottiene file XML aggiornato."
    },
    'swap_coordinates': {
        'en': "Replace x, y coordinates of lmk input file with new ones read in csv input file. Return a lmk updated file as outputfile.",
        'it': "Passare come primo input il file LMK, poi il file TXT/CSV dei punti e delle loro coordinate.\nIn output si ottiene il file LMK aggiornato.",
    },
    'out_to_dxf': {
        'en': "Create a DXF file from a OUT one.",
        'it': "Passare in input un file OUT. In output si ottiene un file DXF creato a partire dalle coordinate del file DXF."
    },
    'translate_lmk': {
        'en': "Translate by given deltas (input via command line) the 2D coordinates in the lmk file.",
        'it': "Passare in input un file LMK da traslare e specificare delta x e delta y. In output si ottiene un file LMK traslato."
    },
    'strip_lmk': {
        'en': 'Strip lmk and return only points and their coordinates.',
        'it': 'Passare in input un file LMK. In output si ottiene un file TXT in formato CSV con i punti e le loro coordinate.'
    },
    'extract_dat': {
        'en': 'Extract point info and write to dat file',
        'it': 'Passare in input il file TXT con i dati sulle stazioni e i punti. In output si ottiene un file in formato DAT con tali info'
    },
}

error_input_msg = "Attenzione! Selezionare file di input."
error_output_msg = "Attenzione! Selezionare file di output."
success_msg = "Operazione completata con successo."


class GeoUtilsMainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        btn_1 = QPushButton('#1: Similitudini', self)
        btn_1.setToolTip(
            '<i>Return a list of same-distance points couples from a file\
             of 2D points.<i>'
        )
        btn_2 = QPushButton('#2: Aggiorna XML', self)
        btn_2.setToolTip(
            '<i>Update an <b>xml</b> file with the points given as input.<i>'
        )
        btn_3 = QPushButton('#3: Aggiorna LMK', self)
        btn_3.setToolTip(
            '<i>Replace x, y coordinates of <b>lmk</b> input file with new ones read\
             in csv input file. Return a lmk updated file as outputfile.<i>'
        )
        btn_4 = QPushButton('#4: Esporta DXF', self)
        btn_4.setToolTip(
            '<i>Create a <b>.DXF</b> file from a <b>.OUT</b> one<i>'
        )
        btn_5 = QPushButton('#5: Trasla LMK', self)
        btn_5.setToolTip(
            '<i>Traslate by given deltas the 2D coordinates in the <b>lmk</b> file.<i>'
        )
        btn_6 = QPushButton('#6: LMK -> TXT', self)
        btn_6.setToolTip(
            '<i>Strip <b>lmk</b> input file to create a txt output file formatted like so: number, coord N, coord E.<i>'
        )
        btn_7 = QPushButton('#6: Stazioni -> DAT', self)
        btn_7.setToolTip(
            '<i>Extract info from <b>txt</b> input file to create a DAT output file.<i>'
        )
        # quit button
        qbtn = QPushButton('Esci', self)
        qbtn.setIcon(QIcon("images/quit_icon.png"))
        qbtn.setStyleSheet("background-color: #d00303; color: #fff")
        qbtn.clicked.connect(QApplication.instance().quit)

        self.grid.addWidget(btn_1, 1, 1)
        self.grid.addWidget(btn_2, 1, 2)
        self.grid.addWidget(btn_3, 2, 1)
        self.grid.addWidget(btn_4, 2, 2)
        self.grid.addWidget(btn_5, 3, 1)
        self.grid.addWidget(btn_6, 3, 2)
        self.grid.addWidget(btn_7, 4, 1)
        self.grid.addWidget(qbtn, 5, 1)

        btn_1.clicked.connect(self.btn1_onclick)
        btn_2.clicked.connect(self.btn2_onclick)
        btn_3.clicked.connect(self.btn3_onclick)
        btn_4.clicked.connect(self.btn4_onclick)
        btn_5.clicked.connect(self.btn5_onclick)
        btn_6.clicked.connect(self.btn6_onclick)
        btn_7.clicked.connect(self.btn7_onclick)

        # windows size and positioning
        self.resize(400, 300)
        self.center()
        self.setWindowTitle('Geoutils GUI')

        self.show()

    def center(self):
        'Centers window according to screen dimensions'
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @pyqtSlot()
    def btn1_onclick(self):
        self.current_win = MatchDistance()
        self.current_win.show()
        self.close()

    @pyqtSlot()
    def btn2_onclick(self):
        self.current_win = XMLFiller()
        self.current_win.show()
        self.close()

    @pyqtSlot()
    def btn3_onclick(self):
        self.current_win = SwapCoordinates()
        self.current_win.show()
        self.close()

    @pyqtSlot()
    def btn4_onclick(self):
        self.current_win = OutToDxf()
        self.current_win.show()
        self.close()

    @pyqtSlot()
    def btn5_onclick(self):
        self.current_win = TranslateLmk()
        self.current_win.show()
        self.close()

    @pyqtSlot()
    def btn6_onclick(self):
        self.current_win = StripLmk()
        self.current_win.show()
        self.close()

    @pyqtSlot()
    def btn7_onclick(self):
        self.current_win = ExtractDat()
        self.current_win.show()
        self.close()


class BaseIOWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        ''' Basic setup for I/O windows. IMPORTANT: call show() method in subclass'''
        self.grid = QGridLayout()
        self.setLayout(self.grid)

        self.error_dialog = QErrorMessage()
        self.success_dialog = QErrorMessage()

        self.input_file_1 = QLineEdit()
        self.input_file_2 = QLineEdit()
        self.output_file = QLineEdit()

        self.btn_input_1 = QPushButton("Seleziona file di input")
        self.btn_input_2 = QPushButton("Seleziona file di input")
        self.btn_output = QPushButton("Seleziona file di output")
        self.btn_mainwindow = QPushButton("Home")
        self.btn_mainwindow.setIcon(QIcon("images/home_icon.png"))
        self.btn_mainwindow.setStyleSheet("background-color: #00abff")
        self.btn_run = QPushButton("Esegui")
        self.btn_run.setIcon(QIcon("images/play_icon.png"))
        self.btn_run.setStyleSheet("background-color: #01942e; color: #fff")

        self.btn_input_1.clicked.connect(self.select_input_file_1)
        self.btn_input_2.clicked.connect(self.select_input_file_2)
        self.btn_output.clicked.connect(self.select_output_file)
        self.btn_run.clicked.connect(self.on_run)
        self.btn_mainwindow.clicked.connect(self.switch_to_mainwindow)

        self.resize(400, 300)
        self.center()
        # self.show()

    def center(self):
        """Centers window according to screen dimensions"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def select_input_file_1(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleziona file", QDir.currentPath(), "")
        # filename, _ = QFileDialog.getOpenFileName(self, "Open file", '/home')
        if filename != "":
            self.input_file_1.setText(filename)

    def select_input_file_2(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Seleziona file", QDir.currentPath(), "")
        if filename != "":
            self.input_file_2.setText(filename)

    def select_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Seleziona file", QDir.currentPath(), "")
        if filename != "":
            self.output_file.setText(filename)

    def on_run(self):
        """ Define method in subclass"""
        return

    def switch_to_mainwindow(self):
        self.current_win = GeoUtilsMainWindow()
        self.current_win.show()
        self.close()


class MatchDistance(BaseIOWindow):

    def initUI(self):
        super().initUI()

        info_label = QLabel(info_labels['match_distance']['it'], self)
        self.btn_input_1.setToolTip(
            '<i>Select 2D coordinates file.<i>'
        )
        self.btn_input_1.resize(self.btn_input_1.sizeHint())
        self.btn_output.setToolTip(
            '<i>Select matching distances output file.<i>'
        )
        self.btn_output.resize(self.btn_output.sizeHint())

        self.grid.addWidget(info_label, 0, 0, 1, 3)
        self.grid.addWidget(self.input_file_1, 1, 1)
        self.grid.addWidget(self.btn_input_1, 1, 2)
        self.grid.addWidget(self.output_file, 2, 1)
        self.grid.addWidget(self.btn_output, 2, 2)
        self.grid.addWidget(self.btn_run, 3, 2)
        self.grid.addWidget(self.btn_mainwindow, 4, 2)

        self.setWindowTitle("script#1: Similitudini")
        self.show()

    def on_run(self):
        input_file = self.input_file_1.text()
        output_file = self.output_file.text()

        if not input_file:
            self.error_dialog.showMessage(error_input_msg)
            return
        if not output_file:
            self.error_dialog.showMessage(error_output_msg)
            return

        points = geoutils.rows2list(open(input_file))

        comb_list = list(combinations(points, 2))

        dist_tuple_list = geoutils.comb2dist_tuple_list(comb_list)

        dup_list = geoutils.get_dup_list(dist_tuple_list)

        with open(output_file, "w+") as f:
            for dup in dup_list:
                f.write("Match!\n#{} ({}, {}) and #{} ({}, {}), dist={:06.3f}\n#{} ({}, {}) and #{} ({}, {}), dist={:06.3f}\n"
                        .format(dup[0][0][0], dup[0][0][1], dup[0][0][2], dup[0][1][0],
                                dup[0][1][1], dup[0][1][2], dup[0][2], dup[1][0][0],
                                dup[1][0][1], dup[1][0][2], dup[1][1][0], dup[1][1][1],
                                dup[1][1][2], dup[1][2],)
                        )
        self.success_dialog.showMessage(success_msg)

class XMLFiller(BaseIOWindow):

    def initUI(self):
        super().initUI()

        info_label = QLabel(info_labels['xml_filler']['it'], self)
        self.btn_input_1.setToolTip(
            '<i>Select XML file.<i>'
        )
        self.btn_input_1.resize(self.btn_input_1.sizeHint())
        self.btn_input_2.setToolTip(
            '<i>Select input points file.<i>'
        )
        self.btn_input_2.resize(self.btn_input_2.sizeHint())
        self.btn_output.setToolTip(
            '<i>Select updated XML output file.<i>'
        )
        self.btn_output.resize(self.btn_output.sizeHint())

        self.grid.addWidget(info_label, 0, 0, 1, 3)
        self.grid.addWidget(self.input_file_1, 1, 1)
        self.grid.addWidget(self.btn_input_1, 1, 2)
        self.grid.addWidget(self.input_file_2, 2, 1)
        self.grid.addWidget(self.btn_input_2, 2, 2)
        self.grid.addWidget(self.output_file, 3, 1)
        self.grid.addWidget(self.btn_output, 3, 2)
        self.grid.addWidget(self.btn_run, 4, 2)
        self.grid.addWidget(self.btn_mainwindow, 5, 2)

        self.setWindowTitle("script#2: Aggiorna XML")
        self.show()

    def on_run(self):
        input_xml = self.input_file_1.text()
        input_points = self.input_file_2.text()
        output_file = self.output_file.text()

        if not input_xml or not input_points:
            self.error_dialog.showMessage(error_input_msg)
            return
        if not output_file:
            self.error_dialog.showMessage(error_output_msg)
            return

        points = geoutils.rows2list(open(input_points))

        fill_xml_dict = geoutils.fill_xml_points(points=points, xml_path=input_xml)

        fill_xml_xml = xmltodict.unparse(fill_xml_dict, pretty=True)

        with open(output_file, "w+") as f:
            f.write(fill_xml_xml)
        self.success_dialog.showMessage(success_msg)


class SwapCoordinates(BaseIOWindow):

    def initUI(self):
        super().initUI()

        info_label = QLabel(info_labels['swap_coordinates']['it'], self)
        self.btn_input_1.setToolTip(
            '<i>Select lmk file.<i>'
        )
        self.btn_input_1.resize(self.btn_input_1.sizeHint())
        self.btn_input_2.setToolTip(
            '<i>Select 2D points csv file.<i>'
        )
        self.btn_input_2.resize(self.btn_input_2.sizeHint())
        self.btn_output.setToolTip(
            '<i>Select updated lmk output file.<i>'
        )
        self.btn_output.resize(self.btn_output.sizeHint())

        self.grid.addWidget(info_label, 0, 0, 1, 3)
        self.grid.addWidget(self.input_file_1, 1, 1)
        self.grid.addWidget(self.btn_input_1, 1, 2)
        self.grid.addWidget(self.input_file_2, 2, 1)
        self.grid.addWidget(self.btn_input_2, 2, 2)
        self.grid.addWidget(self.output_file, 3, 1)
        self.grid.addWidget(self.btn_output, 3, 2)
        self.grid.addWidget(self.btn_run, 4, 2)
        self.grid.addWidget(self.btn_mainwindow, 5, 2)

        self.setWindowTitle("script#3: Aggiorna LMK")
        self.show()

    def on_run(self):
        input_lmk = self.input_file_1.text()
        input_points = self.input_file_2.text()
        output_file = self.output_file.text()

        if not input_lmk or not input_points:
            self.error_dialog.showMessage(error_input_msg)
            return
        if not output_file:
            self.error_dialog.showMessage(error_output_msg)
            return

        header, rows_data = geoutils.lmk2csv(open(input_lmk))

        swapped_rows = geoutils.swap_csv_coordinates(input_points, rows_data)

        with open(output_file, 'w+') as f:
            f.write('\n'.join(header))
            f.write('\n')
            for fr in swapped_rows:
                f.write(fr[0])
                f.write(str(fr[1]).rjust(10))
                f.write(str(fr[2]).rjust(10))
                f.write(str(fr[3]).rjust(5))
                f.write(str(fr[4]).rjust(8))
                f.write(str(fr[5]).rjust(9))
                f.write(str(fr[6]).rjust(7))
                f.write(str(fr[7]).rjust(7))
                f.write(str(fr[8]).rjust(7))
                f.write('\n')
        self.success_dialog.showMessage(success_msg)

class OutToDxf(BaseIOWindow):

    def initUI(self):
        super().initUI()

        info_label = QLabel(info_labels['out_to_dxf']['it'], self)
        self.btn_input_1.setToolTip(
            '<i>Select input <b>.out</b> file.<i>'
        )
        self.btn_input_1.resize(self.btn_input_1.sizeHint())
        self.btn_output.setToolTip(
            '<i>Select <b>.dxf</b> output file.<i>'
        )
        self.btn_output.resize(self.btn_output.sizeHint())

        self.grid.addWidget(info_label, 0, 0, 1, 3)
        self.grid.addWidget(self.input_file_1, 1, 1)
        self.grid.addWidget(self.output_file, 2, 1)
        self.grid.addWidget(self.btn_input_1, 1, 2)
        self.grid.addWidget(self.btn_output, 2, 2)
        self.grid.addWidget(self.btn_run, 3, 2)
        self.grid.addWidget(self.btn_mainwindow, 4, 2)

        self.setWindowTitle("script#4: Esporta DXF")
        self.show()

    def on_run(self):
        outfile = self.input_file_1.text()
        output_file = self.output_file.text()

        if not outfile:
            self.error_dialog.showMessage(error_input_msg)
            return
        if not output_file:
            self.error_dialog.showMessage(error_output_msg)
            return

        height = 0.07
        layer_1 = 1  # layer points
        layer_2 = 2  # layer text

        # setting up header
        header = "  0\nSECTION\n2\nHEADER\n  9\n$PDSIZE\n 40\n2.0\n  9\n$PDMODE\n 70\n30\n  9\n$TEXTSIZE\n 40\n.02\n  9\n$TEXTSTYLE\n  7\nSTANDARD\n  0\nENDSEC\n  0\nSECTION\n2\nENTITIES"
        footer = "\n0\nENDSEC\n0\nEOF"
        # setting up entity base format
        base_format = "\n0\nPOINT\n8\n{layer_1}\n10\n{est}\n20\n{nord}\n0\nTEXT\n8\n{layer_2}\n10\n{est}\n20\n{nord}\n40\n{altezza}\n1\n{name}"

        with open(outfile) as out_file:
            # read .out file
            out_reader = csv.reader(out_file, delimiter=',')
            # jump first 4 lines
            for i in range(4):
                next(out_reader)

            # formatted string will stored here and then written to file.
            out_array = []

            for row in out_reader:
                entity = base_format.format(layer_1=layer_1, layer_2=layer_2,
                                            est=geoutils.convert_to_point(row[1]),
                                            nord=geoutils.convert_to_point(row[3]),
                                            altezza=height, name=row[0])
                out_array.append(entity)

        with open(output_file, 'w+') as f:
            f.write(header)
            for ent in out_array:
                f.write(ent)
            f.write(footer)
        self.success_dialog.showMessage(success_msg)


class TranslateLmk(BaseIOWindow):

    def initUI(self):
        super().initUI()

        info_label = QLabel(info_labels['translate_lmk']['it'], self)
        self.delta_x = QLineEdit(self)
        delta_x_lbl = QLabel(self)
        delta_x_lbl.setText("delta X:")
        self.delta_y = QLineEdit(self)
        delta_y_lbl = QLabel(self)
        delta_y_lbl.setText("delta Y:")

        self.btn_input_1.setToolTip(
            '<i>Select input <b>.lmk</b> file.<i>'
        )
        self.btn_input_1.resize(self.btn_input_1.sizeHint())
        self.btn_output.setToolTip(
            '<i>Select translated <b>.lmk</b> output file.<i>'
        )
        self.btn_output.resize(self.btn_output.sizeHint())

        self.grid.addWidget(info_label, 0, 0, 1, 3)
        self.grid.addWidget(self.input_file_1, 1, 1)
        self.grid.addWidget(self.btn_input_1, 1, 2)
        self.grid.addWidget(self.output_file, 2, 1)
        self.grid.addWidget(self.btn_output, 2, 2)
        self.grid.addWidget(delta_x_lbl, 3, 1)
        self.grid.addWidget(self.delta_x, 3, 2)
        self.grid.addWidget(delta_y_lbl, 4, 1)
        self.grid.addWidget(self.delta_y, 4, 2)
        self.grid.addWidget(self.btn_run, 5, 2)
        self.grid.addWidget(self.btn_mainwindow, 6, 2)

        self.setWindowTitle("script#5: Trasla LMK")
        self.show()

    def on_run(self):
        input_lmk = self.input_file_1.text()
        output_file = self.output_file.text()

        if not input_lmk:
            self.error_dialog.showMessage(error_input_msg)
            return
        if not output_file:
            self.error_dialog.showMessage(error_output_msg)
            return

        header, rows_data = geoutils.lmk2csv(open(input_lmk))

        delta_x = self.delta_x.text()
        delta_y = self.delta_y.text()

        trans_rows = geoutils.trans_coordinates(delta_x, delta_y, rows_data)

        with open(output_file, 'w+') as file:
            file.write('\n'.join(header))
            file.write('\n')
            for row in trans_rows:
                file.write(row[0])
                file.write(str(row[1]).rjust(10))
                file.write(str(row[2]).rjust(10))
                file.write(str(row[3]).rjust(5))
                file.write(str(row[4]).rjust(8))
                file.write(str(row[5]).rjust(9))
                file.write(str(row[6]).rjust(7))
                file.write(str(row[7]).rjust(7))
                file.write(str(row[8]).rjust(7))
                file.write('\n')
        self.success_dialog.showMessage(success_msg)

class StripLmk(BaseIOWindow):
    def initUI(self):
        super().initUI()

        info_label = QLabel(info_labels['strip_lmk']['it'], self)
        self.btn_input_1.setToolTip(
            '<i>Select lmk file.<i>'
        )
        self.btn_input_1.resize(self.btn_input_1.sizeHint())
        self.btn_output.setToolTip(
            '<i>Select name of txt output file.<i>'
        )
        self.btn_output.resize(self.btn_output.sizeHint())

        self.grid.addWidget(info_label, 0, 0, 1, 3)
        self.grid.addWidget(self.input_file_1, 1, 1)
        self.grid.addWidget(self.btn_input_1, 1, 2)
        self.grid.addWidget(self.output_file, 2, 1)
        self.grid.addWidget(self.btn_output, 2, 2)
        self.grid.addWidget(self.btn_run, 3, 2)
        self.grid.addWidget(self.btn_mainwindow, 4, 2)

        self.setWindowTitle('script#6: LMK -> TXT')
        self.show()

    def on_run(self):
        input_file = self.input_file_1.text()
        output_file = self.output_file.text()

        if not input_file:
            self.error_dialog.showMessage(error_input_msg)
            return
        if not output_file:
            self.error_dialog.showMessage(error_output_msg)
            return

        header, rows_data = geoutils.lmk2csv(open(input_file))

        with open(output_file, 'w+') as f:
            for row in rows_data:
                f.write(row[0].lstrip("0"))
                f.write(",")
                f.write(row[1])
                f.write(",")
                f.write(row[2])
                f.write(",")
                f.write('\n')
        self.success_dialog.showMessage(success_msg)


class ExtractDat(BaseIOWindow):

    def initUI(self):
        super().initUI()

        info_label = QLabel(info_labels['extract_dat']['it'], self)
        self.btn_input_1.setToolTip(
            '<i>Select TXT file.<i>'
        )
        self.btn_input_1.resize(self.btn_input_1.sizeHint())
        self.btn_output.setToolTip(
            '<i>Select DAT output file.<i>'
        )
        self.btn_output.resize(self.btn_output.sizeHint())

        self.grid.addWidget(info_label, 0, 0, 1, 3)
        self.grid.addWidget(self.input_file_1, 1, 1)
        self.grid.addWidget(self.btn_input_1, 1, 2)
        self.grid.addWidget(self.output_file, 2, 1)
        self.grid.addWidget(self.btn_output, 2, 2)
        self.grid.addWidget(self.btn_run, 3, 2)
        self.grid.addWidget(self.btn_mainwindow, 4, 2)

        self.setWindowTitle("script#7: Stazioni -> DAT")
        self.show()

    def on_run(self):
        input_file = self.input_file_1.text()
        output_file = self.output_file.text()

        if not input_file:
            self.error_dialog.showMessage(error_input_msg)
            return
        if not output_file:
            self.error_dialog.showMessage(error_output_msg)
            return

        with open(input_file, 'r') as stations_file:
            extract_lst = []
            for line in stations_file:
                if not line.strip():
                    continue
                else:
                    split_line = line.split()
                    if (len(split_line) == 3
                            and split_line[0] == "Nome"
                            and split_line[1] == "Stazione:"):
                        extract_lst.append("s")
                        extract_lst.append(split_line[2])
                    if len(split_line) >= 6 and geoutils.represents_int(split_line[0]):
                        extract_lst.append("p")
                        extract_lst.append(line.split()[0])
                        extract_lst.append(line.split()[4])
                        extract_lst.append(line.split()[5])

        with open(output_file, 'w+') as dat_file:
            for index, el in enumerate(extract_lst):
                if el == "s":
                    dat_file.write("1")
                    dat_file.write("|")
                    dat_file.write(extract_lst[index + 1])
                    dat_file.write("|")
                    dat_file.write("\n")
                elif el == "p":
                    dat_file.write("2")
                    dat_file.write("|")
                    for i in range(1, 4):
                        dat_file.write(extract_lst[index + i])
                        dat_file.write("|")
                    dat_file.write("\n")
        self.success_dialog.showMessage(success_msg)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    geo_main = GeoUtilsMainWindow()
    # script_1 = MatchDistance()
    # script_2 = XMLFiller()
    # script_3 = SwapCoordinates()
    # script_4 = OutToDxf()
    # script_5 = TranslateLmk()
    sys.exit(app.exec_())
