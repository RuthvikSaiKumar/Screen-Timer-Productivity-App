from PySide6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World")
        self.setGeometry(200, 100, 600, 600)
        self.setMinimumSize(600, 600)
