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

class FinalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName('FinalWindow')
        self.setWindowTitle('GeneGenius')

        self.layout = QVBoxLayout(self)
        text = QLabel(self.get_instructions())
        text.setFont(QFont("Arial", 18))
        text.setObjectName('InstructionsText')
        self.layout.addWidget(text, alignment = Qt.AlignCenter)

        ok = QPushButton(text='OK')
        ok.clicked.connect(self.close)
        self.layout.addWidget(ok, alignment=Qt.AlignCenter)

    def get_instructions(self):
        file = 'src/data/final_remarks.txt'
        with open(file) as f:
            instructions = f.read()
        return instructions