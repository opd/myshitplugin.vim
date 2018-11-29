#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import tempfile
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QVBoxLayout,
                             QWidget)

# TODO use shlex
# Check files with ()'""'[] etc.

def get_file_markup(fname, from_line, to_line):
    if False:
        tmp_file = tempfile.NamedTemporaryFile(suffix=".html")
        output_file = tmp_file.name
    output_file = '/tmp/file.html'
    cmd = "pygmentize -f html -O style=colorful,linenos=1 -l python -o %s %s" % (output_file, fname)
    os.system(cmd)
    import pdb;pdb.set_trace()


class MainWindow(QMainWindow):
    def __init__(self, argv):
        super().__init__()
        self._argv = argv
        self.init_ui()

    @property
    def file_name(self):
        return self.argv[1]

    def init_ui(self):
        self.statusBar().showMessage('Ready')
        self.setGeometry(640, 480, 250, 150)
        self.setWindowTitle('Statusbar')
        widget = QWidget()
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        label = QLabel(str(self._argv))
        main_layout.addWidget(label)

        self.setLayout(main_layout)
        self.show()


if __name__ == '__main__':
    get_file_markup(*sys.argv[1:])

    if False:
        app = QApplication(sys.argv)
        main = MainWindow(sys.argv)
        sys.exit(app.exec_())
