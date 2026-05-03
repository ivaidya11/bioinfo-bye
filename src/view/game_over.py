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

class GameOverWindow(QWidget):
    def __init__(self, grade: Grade):
        super().__init__()
        self.grade = grade
        self.setObjectName('GameOverWindow')
        self.setWindowTitle('GeneGenius')

        self.layout = QVBoxLayout(self)
        text = QLabel(self.get_instructions())
        text.setFont(QFont("Arial", 18))
        text.setObjectName('InstructionsText')
        self.layout.addWidget(text, alignment=Qt.AlignCenter)

        restart = QPushButton(text='Restart')
        restart.clicked.connect(self.restart_game)
        self.layout.addWidget(restart, alignment=Qt.AlignCenter)

        ok = QPushButton(text='Quit')
        ok.clicked.connect(self.close)
        self.layout.addWidget(ok, alignment=Qt.AlignCenter)

    def restart_game(self):
        from view.main_window import MainWindow
        from models.sequence_file import SequenceFile
        seqs_file = 'src/data/seqs_3.txt' if self.grade == Grade.THIRD else 'src/data/seqs_5.txt'
        self.main_window = MainWindow()
        self.main_window.showMaximized()
        self.main_window.set_box_labels(self.grade)
        seqs = SequenceFile(seqs_file)
        self.main_window.start_string_feed(seqs.get_shuffled_list(), initial_delay_ms=3000, acceleration=0.99)
        self.close()

    def get_instructions(self):
        file = 'src/data/game_over_text.txt'
        with open(file) as f:
            instructions = f.read()
        return instructions