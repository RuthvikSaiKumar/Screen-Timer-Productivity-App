from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import *
import PySide6.QtCharts as QtCharts

import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hello World")
        self.setGeometry(100, 100, 300, 300)

        self.slider = QSlider(self)
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(50)
        self.slider.setGeometry(50, 50, 200, 30)

        self.slider.valueChanged.connect(self.slider_value_changed)

        self.chart = QtCharts.QChart()
        self.chart.setTitle("Hello World")
        self.chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        # dark theme
        self.chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)

        self.series = QtCharts.QLineSeries()
        self.series.append(0, 0)
        self.series.append(1, 1)
        self.series.append(2, 1)
        self.series.append(3, 2)
        self.series.append(4, 3)
        self.series.append(5, 5)
        self.series.append(6, 8)
        self.series.append(7, 13)
        self.series.append(8, 21)
        self.series.append(9, 34)
        self.series.append(10, 55)

        self.chart.addSeries(self.series)

        self.axis_x = QtCharts.QValueAxis()
        self.axis_x.setLabelFormat("%i")
        self.axis_x.setTitleText("X Axis")
        self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(self.axis_x)

        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setLabelFormat("%i")
        self.axis_y.setTitleText("Y Axis")
        self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(self.axis_y)

        self.chart_view = QtCharts.QChartView(self.chart, self)
        self.chart_view.setGeometry(50, 100, 200, 150)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        check = QCheckBox("Check", self)
        check.stateChanged.connect(lambda: print(check.isChecked()))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.chart_view)
        self.layout.addWidget(check)
        self.setLayout(self.layout)

    @staticmethod
    def slider_value_changed(value):
        print(value)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
