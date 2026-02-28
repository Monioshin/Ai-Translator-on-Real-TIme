from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal, QPoint

class MiniWindow(QWidget):
    toggle_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self._old_pos = None

    def init_ui(self):
        # Настройки Mac: поверх всех, без рамок
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(220, 160)
        
        # Основной контейнер
        self.main_widget = QWidget(self)
        self.main_widget.setObjectName("MainWidget")
        self.main_widget.setFixedSize(220, 160)
        
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(15, 10, 15, 15)
        layout.setSpacing(10)

        title = QLabel("AI TRANSLATOR")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 10px; font-weight: bold; color: #6272a4; letter-spacing: 1px; background: transparent;")
        layout.addWidget(title)
        
        self.label = QLabel("СТАТУС: ВЫКЛ")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 12px; font-weight: bold; color: #ff5555; background: transparent;")
        layout.addWidget(self.label)

        self.lang_choice = QComboBox()
        self.lang_choice.addItems(["RU ➔ EN", "EN ➔ RU"])
        layout.addWidget(self.lang_choice)

        self.btn = QPushButton("ЗАПУСТИТЬ")
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.on_click)
        layout.addWidget(self.btn)

        self.setStyleSheet("""
            #MainWidget {
                background-color: #1e1f29;
                border: 1px solid #44475a;
                border-radius: 20px;
            }
            QComboBox {
                background-color: #282a36;
                color: #f8f8f2;
                border: 1px solid #44475a;
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton {
                background-color: #44475a;
                color: #f8f8f2;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #50fa7b;
                color: #282a36;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self._old_pos is not None:
            delta = event.globalPosition().toPoint() - self._old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self._old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self._old_pos = None

    def on_click(self):
        active = self.btn.isChecked()
        self.label.setText("СТАТУС: РАБОТАЕТ" if active else "СТАТУС: ВЫКЛ")
        self.label.setStyleSheet(f"font-size: 12px; font-weight: bold; color: {'#50fa7b' if active else '#ff5555'}; background: transparent;")
        self.btn.setText("ОСТАНОВИТЬ" if active else "ЗАПУСТИТЬ")
        self.toggle_signal.emit(active)