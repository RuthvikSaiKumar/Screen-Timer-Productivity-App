from PySide6.QtWidgets import QApplication
import graphics
import sys

app = QApplication(sys.argv)
window = graphics.MainWindow()

window.show()
app.exec()
