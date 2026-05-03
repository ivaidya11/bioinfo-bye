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
    def __init__(self, minutes=0, seconds=0, score=0):
        super().__init__()
        self.setObjectName('FinalWindow')
        self.setWindowTitle('GeneGenius')

        self.layout = QVBoxLayout(self)
        text = QLabel(self.get_instructions())
        text.setFont(QFont("Arial", 18))
        text.setObjectName('InstructionsText')
        self.layout.addWidget(text, alignment=Qt.AlignCenter)
        time_label = QLabel(f"Time: {minutes:02d}:{seconds:02d}")
        time_font = QFont("Arial", 30)
        time_font.setBold(True)
        time_label.setFont(time_font)
        self.layout.addWidget(time_label, alignment=Qt.AlignCenter)
        score_label = QLabel(f"Score: {score}")
        score_font = QFont("Arial", 30)
        score_font.setBold(True)
        score_label.setFont(score_font)
        self.layout.addWidget(score_label, alignment=Qt.AlignCenter)
        ok = QPushButton(text='OK')
        ok.clicked.connect(self.close)
        self.layout.addWidget(ok, alignment=Qt.AlignCenter)

    def get_instructions(self):
        file = 'src/data/final_remarks.txt'
        with open(file) as f:
            instructions = f.read()
        return instructions