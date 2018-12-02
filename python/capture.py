#!/usr/bin/python3
# -*- coding: utf-8 -*-

import functools
import os
import re
import subprocess
import sys
import tempfile
from PyQt5.QtWidgets import (QApplication, QComboBox, QFileDialog, QLabel,
                             QMainWindow, QPushButton, QVBoxLayout, QWidget)
from PyQt5.QtWebEngineWidgets import QWebEngineView as QWebView
from PyQt5.QtCore import QRect

# TODO change font size
# TODO capture widget to image
# TODO use shlex
# Check files with ()'""'[] etc.
# TODO log sys.argvs call params and time


def before_settrace():
    import PyQt5
    PyQt5.QtCore.pyqtRemoveInputHook()


def command_results(cmd):
    cmd = cmd.split(' ')
    data = subprocess.check_output(cmd)
    data = data.decode('utf-8')
    data = data.split('\n')
    return data


def get_file_markup(fname, from_line, to_line):
    from_line = int(from_line)
    to_line = int(to_line)
    tmp_file = tempfile.NamedTemporaryFile(suffix=".html")
    output_file = tmp_file.name
    # output_file = '/tmp/file.html'
    cmd = "pygmentize -f html -O style=colorful -l python -o %s %s" % (
        output_file,
        fname,
    )
    os.system(cmd)
    lines = []
    with open(output_file) as f:
        lines = f.readlines()
    begin_line = '<div class="highlight"><pre>'
    assert lines[0].startswith(begin_line)
    lines[0] = lines[0][len(begin_line):]
    lines.pop(-1)
    from_line -= 1
    to_line -= 1
    assert 0 <= from_line <= to_line < len(lines)
    lines = lines[from_line:to_line + 1]
    lines = [
        '<span class="n">%s</span>  %s' % (i, line)
        for i, line in enumerate(lines, from_line + 1)
    ]
    return lines


DEFAULT_CSS = """
.hll { background-color: #49483e }
.c { color: #75715e } /* Comment */
.err { color: #960050; background-color: #1e0010 } /* Error */
.k { color: #66d9ef } /* Keyword */
.l { color: #ae81ff } /* Literal */
.n { color: #f8f8f2 } /* Name */
.o { color: #f92672 } /* Operator */
.p { color: #f8f8f2 } /* Punctuation */
.cm { color: #75715e } /* Comment.Multiline */
.cp { color: #75715e } /* Comment.Preproc */
.c1 { color: #75715e } /* Comment.Single */
.cs { color: #75715e } /* Comment.Special */
.ge { font-style: italic } /* Generic.Emph */
.gs { font-weight: bold } /* Generic.Strong */
.kc { color: #66d9ef } /* Keyword.Constant */
.kd { color: #66d9ef } /* Keyword.Declaration */
.kn { color: #f92672 } /* Keyword.Namespace */
.kp { color: #66d9ef } /* Keyword.Pseudo */
.kr { color: #66d9ef } /* Keyword.Reserved */
.kt { color: #66d9ef } /* Keyword.Type */
.ld { color: #e6db74 } /* Literal.Date */
.m { color: #ae81ff } /* Literal.Number */
.s { color: #e6db74 } /* Literal.String */
.na { color: #a6e22e } /* Name.Attribute */
.nb { color: #f8f8f2 } /* Name.Builtin */
.nc { color: #a6e22e } /* Name.Class */
.no { color: #66d9ef } /* Name.Constant */
.nd { color: #a6e22e } /* Name.Decorator */
.ni { color: #f8f8f2 } /* Name.Entity */
.ne { color: #a6e22e } /* Name.Exception */
.nf { color: #a6e22e } /* Name.Function */
.nl { color: #f8f8f2 } /* Name.Label */
.nn { color: #f8f8f2 } /* Name.Namespace */
.nx { color: #a6e22e } /* Name.Other */
.py { color: #f8f8f2 } /* Name.Property */
.nt { color: #f92672 } /* Name.Tag */
.nv { color: #f8f8f2 } /* Name.Variable */
.ow { color: #f92672 } /* Operator.Word */
.w { color: #f8f8f2 } /* Text.Whitespace */
.mf { color: #ae81ff } /* Literal.Number.Float */
.mh { color: #ae81ff } /* Literal.Number.Hex */
.mi { color: #ae81ff } /* Literal.Number.Integer */
.mo { color: #ae81ff } /* Literal.Number.Oct */
.sb { color: #e6db74 } /* Literal.String.Backtick */
.sc { color: #e6db74 } /* Literal.String.Char */
.sd { color: #e6db74 } /* Literal.String.Doc */
.s2 { color: #e6db74 } /* Literal.String.Double */
.se { color: #ae81ff } /* Literal.String.Escape */
.sh { color: #e6db74 } /* Literal.String.Heredoc */
.si { color: #e6db74 } /* Literal.String.Interpol */
.sx { color: #e6db74 } /* Literal.String.Other */
.sr { color: #e6db74 } /* Literal.String.Regex */
.s1 { color: #e6db74 } /* Literal.String.Single */
.ss { color: #e6db74 } /* Literal.String.Symbol */
.bp { color: #f8f8f2 } /* Name.Builtin.Pseudo */
.vc { color: #f8f8f2 } /* Name.Variable.Class */
.vg { color: #f8f8f2 } /* Name.Variable.Global */
.vi { color: #f8f8f2 } /* Name.Variable.Instance */
.il { color: #ae81ff } /* Literal.Number.Integer.Long */
"""


class MainWindow(QMainWindow):
    def __init__(self, argv):
        super().__init__()
        self._argv = argv
        self._current_style = 'monokai'
        self._line_count = 0
        self.init_ui()

    @property
    def file_name(self):
        return self._argv[1]

    @property
    def from_line(self):
        return int(self._argv[2])

    @property
    def to_line(self):
        return int(self._argv[3])

    @functools.lru_cache(maxsize=128)
    def get_style_css(self, style_name):
        lines = command_results("pygmentize -S %s -f html" % style_name)
        return "\n".join(lines)

    def get_styles(self):
        pattern = re.compile(r"^[*] ([a-z]+):$")
        lines = command_results("pygmentize -L -- styles")
        lines = (pattern.match(line) for line in lines)
        lines = (line.group(1) for line in lines if line)
        lines = list(lines)
        return lines

    def style_changed(self, style):
        self._current_style = style
        self.update_html()

    def update_html(self):
        lines = get_file_markup(self.file_name,
                                self.from_line,
                                self.to_line)
        self._line_count = len(lines)
        html = "".join(lines)
        css = self.get_style_css(self._current_style)
        beforeCode = """
        <html>
            <head>
                <style>%s
                body {
                  margin: 0;
                  font-size: 16px;
                }
                .hll {
                    // padding: 5px;
                }
                </style>
            </head>
        <body>
            <div class="hll"><pre>"""
        beforeCode = beforeCode % css
        afterCode = """</pre>
                </div>
            </body>
        </html>"""
        html = beforeCode + html + afterCode
        self.web_view.setHtml(html)
        self.web_view.setZoomFactor(1.0)

    def on_capture_clicked(self):
        print("HOP")
        img = self.web_view.grab()
        before_settrace()
        rect = QRect(0, 0, img.width(), self._line_count * 16);
        img = img.copy(rect);
        fileName = QFileDialog.getSaveFileName(
            self, "Caption", "/tmp/", "Image Files (*.png, *.jpg *.bmp)")
        img.save(fileName)

    def init_ui(self):
        self.statusBar().showMessage('Ready')
        self.setGeometry(640, 480, 640, 480)
        self.setWindowTitle('Statusbar')
        widget = QWidget()
        main_layout = QVBoxLayout()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        label_str = str(self._argv)
        label_str = "Label"
        label = QLabel(label_str)
        main_layout.addWidget(label)

        self.web_view = QWebView()
        self.update_html()
        main_layout.addWidget(self.web_view)

        styles = self.get_styles()
        self.color_cbox = QComboBox()
        for style in styles:
            self.color_cbox.addItem(style)
        main_layout.addWidget(self.color_cbox)
        self.color_cbox.currentTextChanged.connect(self.style_changed)

        self.capture_btn = QPushButton("Take Screenshot")
        self.capture_btn.clicked.connect(self.on_capture_clicked)
        main_layout.addWidget(self.capture_btn)

        self.setLayout(main_layout)
        self.show()


if __name__ == '__main__':
    # get_file_markup(*sys.argv[1:])

    if True:
        app = QApplication(sys.argv)
        main = MainWindow(sys.argv)
        sys.exit(app.exec_())
