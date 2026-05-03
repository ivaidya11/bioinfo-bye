import sys
from typing import List
from PySide6.QtWidgets import (
    QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFrame, QSizePolicy, QScrollArea
)
from PySide6.QtCore import Qt, QMimeData, QTimer, Signal
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QDrag, QMouseEvent, QPixmap
from view.info_window import InfoWindow
from view.final_window import FinalWindow

class DraggableLabel(QLabel): #This represents a DNA sequence block that the player can drag.
    def __init__(self, text):
        super().__init__(text)
        self.setText(text)
        self.setObjectName("DraggableLabel")
        self.setProperty("class", "DraggableLabel")
        self.setAlignment(Qt.AlignCenter)
        self.setFixedHeight(40)
        self.setStyleSheet("")
        self.setAttribute(Qt.WA_DeleteOnClose)  # Optional: auto-delete if removed

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.text())
            drag.setMimeData(mime_data)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            # Hide temporarily to avoid flicker
            self.hide()
            result = drag.exec(Qt.MoveAction)

            # If dropped, delete self
            if result == Qt.MoveAction:
                self.setParent(None)
                self.deleteLater()
            else:
                self.show()


class DropBox(QFrame):
    wrong_drop = Signal(str) #new 

    def __init__(self, placeholder="Drop here"):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("DropBox")
        self.setProperty("class", "DropBox")
        self.setMinimumHeight(150)

        self.group = None #new 
        self.contents: list[str] = [] #new 

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(5)

        self.label_widget = QLabel("") #new
        self.label_widget.setAlignment(Qt.AlignCenter) #new
        self.layout.addWidget(self.label_widget) #new

        self.placeholder = QLabel(placeholder)
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setStyleSheet("color: #aaa; font-style: italic;")
        self.layout.addWidget(self.placeholder)

    def set_label(self, text: str): #new 
        self.label_widget.setText(text)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        text = event.mimeData().text()
        event.setDropAction(Qt.MoveAction) 
        event.accept()  

        if self.seq_to_group.get(text) != self.group: #new
            self.wrong_drop.emit(text)
            return

        self.contents.append(text)

        # Remove placeholder if present
        if self.placeholder:
            self.placeholder.deleteLater()
            self.placeholder = None

        block = DraggableLabel(text)
        self.layout.addWidget(block)


class SpawningBox(QFrame):
    """Container for stacking draggable string blocks."""
    def __init__(self):
        super().__init__()
        self.setObjectName("SpawningBox")
        self.setProperty("class", "SpawningBox")
        self.setFixedHeight(200)
        self.setAcceptDrops(False)

        # Scrollable container in case blocks overflow
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)
        self.scroll.viewport().setObjectName("qt_scrollarea_viewport")
        self.scroll.viewport().setStyleSheet("background-color: rgb(45, 3, 117);")

        container = QWidget()
        self.layout = QVBoxLayout(container)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(5)
        self.scroll.setWidget(container)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.scroll)

    def add_string_block(self, text: str):
        block = DraggableLabel(text)
        block.setStyleSheet("background-color: rgb(223, 165, 20);")
        self.layout.addWidget(block)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.setWindowTitle("Gene Genius")
        self.setMinimumSize(800, 600)

        self.string_list = []
        self.string_timer = QTimer(self)
        self.string_index = 0
        self.current_delay = 0
        self.acceleration = 1.0

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.setup_top_banner()
        self.setup_spawning_box()
        self.setup_lower_drop_zone()
        self.setup_bottom_bar()

        # replacing counter with stopwatch
        self._elapsed_seconds = 0
        self._stopwatch_timer = QTimer(self)
        self._stopwatch_timer.setInterval(1000)
        self._stopwatch_timer.timeout.connect(self._tick_stopwatch)

        self.info_window = None

        self.lives = 3 #new 

    def setup_top_banner(self):
        banner = QFrame()
        banner.setObjectName("TopBanner")
        banner_layout = QHBoxLayout(banner)
        banner_layout.setContentsMargins(10, 5, 10, 5)

        self.counter_label = QLabel("Time: 00:00")
        self.counter_label.setStyleSheet("font-weight: bold;")  # You can move this to QSS if needed
        self.title_label = QLabel("Gene Genius")
        self.title_label.setObjectName("title_label")
        self.status_label = QLabel("3rd grade")

        self.heart_labels = [] #new 
        for _ in range(3): #new 
            heart = QLabel("♥")
            heart.setStyleSheet("color: red; font-size: 20px;")
            self.heart_labels.append(heart)

        banner_layout.addWidget(self.status_label, alignment=Qt.AlignLeft)
        banner_layout.addStretch()
        banner_layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        banner_layout.addStretch()
        for heart in self.heart_labels: #new 
            banner_layout.addWidget(heart)
        banner_layout.addWidget(self.counter_label, alignment=Qt.AlignRight)

        self.main_layout.addWidget(banner)

    def setup_spawning_box(self):
        self.spawning_box = SpawningBox()
        self.main_layout.addWidget(self.spawning_box)

    def setup_lower_drop_zone(self):
        lower_zone_layout = QHBoxLayout()
        lower_zone_layout.setSpacing(20)
        lower_zone_layout.setContentsMargins(10, 10, 10, 10)

        # Left container
        left_container = QFrame()
        left_layout = QVBoxLayout()
        left_layout.setSpacing(20)  # vertical spacing between boxes
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setAlignment(Qt.AlignTop)
        self.left_drop_box = DropBox("Left 1")
        self.left_drop_box.setObjectName('LeftTopBox')
        left_layout.addWidget(self.left_drop_box)
        self.left2_drop_box = DropBox("Left 2")
        self.left2_drop_box.setObjectName('LeftBotBox')
        left_layout.addWidget(self.left2_drop_box)
        left_container.setLayout(left_layout)
        left_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Right container
        right_container = QFrame()
        right_layout = QVBoxLayout()
        right_layout.setSpacing(20)  # vertical spacing between boxes
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setAlignment(Qt.AlignTop)
        self.right_drop_box = DropBox("Right 1")
        self.right_drop_box.setObjectName('RightTopBox')
        right_layout.addWidget(self.right_drop_box)
        self.right2_drop_box = DropBox("Right 2")
        self.right2_drop_box.setObjectName('RightBotBox')
        right_layout.addWidget(self.right2_drop_box)
        right_container.setLayout(right_layout)
        right_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Make both take equal width
        lower_zone_layout.addWidget(left_container, stretch=1)
        lower_zone_layout.addWidget(right_container, stretch=1)

        self.main_layout.addLayout(lower_zone_layout)

    def setup_bottom_bar(self):
        footer = QFrame()
        footer.setObjectName("BottomBanner")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(10, 5, 10, 5)

        self.left_button = QPushButton("Info")
        self.left_button.clicked.connect(self.launch_info)
        self.center_button = QPushButton("Analyze")
        self.right_button = QPushButton("Finish")
        self.right_button.clicked.connect(self.final_remarks)

        footer_layout.addWidget(self.left_button, alignment=Qt.AlignLeft)
        footer_layout.addStretch()
        footer_layout.addWidget(self.center_button, alignment=Qt.AlignCenter)
        footer_layout.addStretch()
        footer_layout.addWidget(self.right_button, alignment=Qt.AlignRight)

        self.main_layout.addWidget(footer)

    def set_box_labels(self, grade): #new
        from models.grade import Grade
        self.grade = grade
        if grade == Grade.THIRD:
            box_file = 'src/data/box_names_3.txt'
            self._seqs_file = 'src/data/seqs_3.txt'
        else:
            box_file = 'src/data/box_names_5.txt'
            self._seqs_file = 'src/data/seqs_5.txt'
        with open(box_file) as f:
            lines = [line.strip() for line in f if not line.startswith('GRADE')]

        # Build seq_to_group from the seqs file
        seq_to_group: dict[str, int] = {}
        current_group = None
        with open(self._seqs_file) as f:
            for raw in f:
                line = raw.strip()
                if line.startswith('GROUP'):
                    current_group = int(line.split()[1])
                elif line and not line.startswith('GRADE'):
                    seq_to_group[line.lstrip('#')] = current_group

        boxes = [self.left_drop_box, self.left2_drop_box, self.right_drop_box, self.right2_drop_box]
        for box, line in zip(boxes, lines):
            group, name = line.split(maxsplit=1)
            box.group = int(group)
            box.seq_to_group = seq_to_group
            box.set_label(name)
            box.wrong_drop.connect(self.lose_life)

    def start_string_feed(self, strings: List[str], initial_delay_ms: int = 1000, acceleration: float = 1.0):
        self.string_list = strings
        self.string_index = 0
        self.current_delay = initial_delay_ms
        self.acceleration = acceleration
        self._stopwatch_timer.start()  # Start the stopwatch when feeding starts

        self.string_timer.timeout.connect(self.feed_next_string)
        self.string_timer.start(self.current_delay)

    def feed_next_string(self):
        if self.string_index < len(self.string_list):
            string = self.string_list[self.string_index]
            self.spawning_box.add_string_block(string)
            self.string_index += 1
            self.current_delay = int(self.current_delay * self.acceleration)
            self.string_timer.start(self.current_delay)
        else:
            self.string_timer.stop()  

    def lose_life(self, text: str): #new
        self.lives -= 1
        if self.heart_labels:
            self.heart_labels[self.lives].hide()
        self.spawning_box.add_string_block(text)
        if self.lives == 0:
            from view.game_over import GameOverWindow
            self.game_over_window = GameOverWindow(self.grade)
            self.game_over_window.show()
            self._stopwatch_timer.stop()

            self.close()

    def _tick_stopwatch(self):
        self_elapsed_seconds += 1
        m, s = divmod(self._elapsed_seconds, 60)
        self.counter_label.setText(f"Time: {m:02d}:{s:02d}")

    def launch_info(self):
        self.info_window = InfoWindow(playing=True, grade=None)
        self.info_window.show()

    def final_remarks(self):
        self.final_window = FinalWindow()
        self.final_window.show()
        self._stopwatch_timer.stop()
        self.close()

