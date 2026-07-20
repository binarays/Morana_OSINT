import sys
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QPixmap

from app.home import MainWindow

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.SplashScreen)
        self.setFixedSize(500, 300)
        self.setStyleSheet("background-color: #1e1e1e; border: 1px solid #333333; border-radius: 10px;")
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)
        
        self.logo = QLabel()
        self.logo.setStyleSheet("border: none; background: transparent;")
        logo_pixmap = QPixmap("app/icons/morana-logo-load.png")
        self.logo.setPixmap(logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.logo.setFixedSize(100, 100)
        layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        
        self.status_label = QLabel("Initializing environment...")
        self.status_label.setStyleSheet("color: #888888; font-family: 'Poppins'; font-size: 13px; font-style: italic; border: none;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        self.messages = [
            "Initializing environment...",
            "Loading engine components...",
            "Starting up subsystems...",
            "Preparing UI...",
            "Ready."
        ]
        self.msg_idx = 0
        
    def update_message(self):
        if self.msg_idx < len(self.messages):
            self.status_label.setText(self.messages[self.msg_idx])
            self.msg_idx += 1

app = QApplication(sys.argv)

splash = SplashScreen()
splash.show()

# animate loading text
for _ in range(5):
    splash.update_message()
    app.processEvents()
    time.sleep(0.4)

window = MainWindow()
window.show()
splash.close()

sys.exit(
    app.exec()
)