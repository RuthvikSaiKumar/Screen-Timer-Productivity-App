from PySide6.QtWidgets import QApplication
import ui
import sys

app = QApplication(sys.argv)
window = ui.MainWindow()

window.show()
app.exec()
