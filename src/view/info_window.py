import sys
from typing import List
from PySide6.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, QMimeData, QTimer
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDrag, QMouseEvent, QPixmap, QFont
from models.grade import Grade
from models.sequence_file import SequenceFile

class InfoWindow(QWidget):
    def __init__(self, playing: bool, grade: Grade|None):
        super().__init__()
        self.setObjectName('InfoWindow')
        self.setWindowTitle('GeneGenius')

        self.layout = QVBoxLayout(self)
        text = QLabel(self.get_instructions())
        text.setFont(QFont("Arial", 18))
        text.setObjectName('InstructionsText')
        self.layout.addWidget(text, alignment = Qt.AlignCenter)

        ok = QPushButton(text='OK')
        self.grade = grade

        if playing:
            ok.clicked.connect(self.close)
        else:
            ok.clicked.connect(self.open_main_window)
        self.layout.addWidget(ok, alignment=Qt.AlignCenter)

    def get_instructions(self):
        file = 'src/data/instructions.txt'
        with open(file) as f:
            instructions = f.read()
        return instructions

    def open_main_window(self):
        from view.main_window import MainWindow

        self.main_window = MainWindow()
        self.main_window.showMaximized()
        self.close()

        if self.grade == Grade.THIRD:
            self.main_window.set_box_labels(self.grade)
            seqs = SequenceFile('src/data/seqs_3.txt')
            l_seqs = seqs.get_shuffled_list()
            self.main_window.start_string_feed(
                l_seqs,
                initial_delay_ms=3000,
                acceleration=0.99
            )
        elif self.grade == Grade.FIFTH:
            self.main_window.set_box_labels(self.grade)
            seqs = SequenceFile('src/data/seqs_5.txt')
            l_seqs = seqs.get_shuffled_list()
            self.main_window.start_string_feed(
                l_seqs,
                initial_delay_ms=3000,
                acceleration=0.96
            )
        else:
            print('Something went wrong. The grade selection failed.')