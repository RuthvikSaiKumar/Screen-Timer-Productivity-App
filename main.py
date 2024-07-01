from PySide6.QtWidgets import QApplication
import ui
import sys
import running

app = QApplication(sys.argv)
window = ui.MainWindow()

running.add_to_startup()

window.show()
app.exec()
