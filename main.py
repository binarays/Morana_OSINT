import sys
from PyQt6.QtWidgets import QApplication
from app.home import MainWindow


app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(
    app.exec()
)