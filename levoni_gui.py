import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QDesktopWidget,
    QMainWindow,
    QLineEdit,
    QGridLayout,
    QFileDialog)
from PyQt5.QtCore import QDir
from itertools import combinations
from geoutils import (
    rows2list,
    comb2dist_tuple_list,
    get_dup_list
)


class GeoUtilsMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # button for script 1: match distance
        btn_1 = QPushButton('#1: Match distance', self)
        btn_1.setToolTip(
            '<i>Return a list of same-distance points couples from a file\
             of 2D points.<i>'
        )
        btn_1.resize(btn_1.sizeHint())
        btn_1.move(20, 20)

        # button for script 2: xml filler
        btn_2 = QPushButton('#2: XML filler', self)
        btn_2.setToolTip(
            '<i>Update an xml file with the points given as input.<i>'
        )
        btn_2.resize(btn_2.sizeHint())
        btn_2.move(20, 80)

        # button for script 3: swap coordinates
        btn_3 = QPushButton('#3: Swap coordinates', self)
        btn_3.setToolTip(
            '<i>Replace x, y coordinates of lmk input file with new ones read\
             in csv input file. Return a lmk updated file as outputfile.<i>'
        )
        btn_3.resize(btn_3.sizeHint())
        btn_3.move(20, 140)

        # button for script 4: out to dxf
        btn_4 = QPushButton('#4: Out to dxf', self)
        btn_4.setToolTip(
            '<i>Create a <b>.DXF</b> file from a <b>.OUT</b> one<i>'
        )
        btn_4.resize(btn_4.sizeHint())
        btn_4.move(220, 20)

        # button for script 5: translate lmk
        btn_5 = QPushButton('#5: Translate lmk', self)
        btn_5.setToolTip(
            '<i>Translate by given deltas the 2D coordinates in the <b>lmk</b> file.<i>'
        )
        btn_5.resize(btn_5.sizeHint())
        btn_5.move(220, 80)

        # quit button
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(20, 200)

        # windows size and positioning
        self.resize(400, 300)
        self.center()
        self.setWindowTitle('Levoni GUI')

        self.show()

    def center(self):
        'Centers window according to screen dimensions'
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class MatchDistanceWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        self.setLayout(grid)

        self.input_file = QLineEdit()
        self.output_file = QLineEdit()

        btn_input = QPushButton("Select input file")
        btn_output = QPushButton("Select output file")
        btn_run = QPushButton("Run")

        grid.addWidget(self.input_file, 1, 1)
        # grid.addWidget(self.file_2, 2, 1)
        grid.addWidget(self.output_file, 2, 1)
        grid.addWidget(btn_input, 1, 2)
        # grid.addWidget(btn2, 2, 2)
        grid.addWidget(btn_output, 2, 2)
        grid.addWidget(btn_run, 3, 2)

        btn_input.clicked.connect(self.select_input_file)
        btn_output.clicked.connect(self.select_output_file)

        btn_run.clicked.connect(self.on_run)

        self.setWindowTitle("script#1: Match distance")
        self.show()

    def select_input_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select Files", QDir.currentPath(), "*.txt")
        # filename, _ = QFileDialog.getOpenFileName(self, "Open file", '/home')
        if filename != "":
            self.input_file.setText(filename)

    # def select_input_file(self):
    #     fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
    #     if fname[0]:
    #         f = open(fname[0], 'r')
    #
    #         with f:
    #             data = f.read()
    #             self.file1.setText(data)

    def select_output_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Select Files", QDir.currentPath(), "*.html")
        if filename != "":
            self.output_file.setText(filename)

    def on_run(self):
        input_file = self.input_file.text()
        output_file = self.output_file.text()

        points = rows2list(open(input_file))

        comb_list = list(combinations(points, 2))

        dist_tuple_list = comb2dist_tuple_list(comb_list)

        dup_list = get_dup_list(dist_tuple_list)

        with open(output_file, "w+") as f:
            for dup in dup_list:
                f.write("Match!\n#{} ({}, {}) and #{} ({}, {}), dist={:06.3f}\n#{} ({}, {}) and #{} ({}, {}), dist={:06.3f}\n"
                        .format(dup[0][0][0], dup[0][0][1], dup[0][0][2], dup[0][1][0],
                                dup[0][1][1], dup[0][1][2], dup[0][2], dup[1][0][0],
                                dup[1][0][1], dup[1][0][2], dup[1][1][0], dup[1][1][1],
                                dup[1][1][2], dup[1][2],)
                        )


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # geo_main = GeoUtilsMainWindow()
    script_1 = MatchDistanceWindow()
    sys.exit(app.exec_())
