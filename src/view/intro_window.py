from PySide6.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QMainWindow, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt, Signal
import sys
from view.info_window import InfoWindow
from models.grade import Grade

class IntroWidow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("IntroWidow")
        self.setWindowTitle('GeneGenius')

        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        title = QLabel(
'''Welcome to GeneGenius!
Are you ready to take on the challenge of a bioinformatician?

Choose your grade level:''')
        title.setObjectName('IntroText')
        layout.addWidget(title)

        buttons = QHBoxLayout()

        third_grade_button = QPushButton('3rd')
        third_grade_button.clicked.connect(self.third_grade)
        buttons.addWidget(third_grade_button)

        fifth_grade_button = QPushButton('5th')
        fifth_grade_button.clicked.connect(self.fifth_grade)
        buttons.addWidget(fifth_grade_button)

        layout.addLayout(buttons)
        self.info_window = None

        layout.setContentsMargins(20,20,20,20)

    def third_grade(self):
        self.info_window = InfoWindow(playing=False, grade=Grade.THIRD)
        self.info_window.show()

    def fifth_grade(self):
        self.info_window = InfoWindow(playing=False, grade=Grade.FIFTH)
        self.info_window.show()