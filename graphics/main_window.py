import PySide6.QtCharts as QtCharts
import PySide6.QtCore
from PySide6.QtGui import QPainter, QIcon
from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget, QSizePolicy, QScrollArea, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ReConnect - Productivity Tracker")
        self.setGeometry(200, 100, 600, 600)
        self.setMinimumSize(650, 600)
        icon = QIcon("assets/ReConnect Logo.png")
        self.setWindowIcon(icon)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        ###############################################################################################

        self.pie = QtCharts.QPieSeries()
        self.pie.append("Work", 10)
        self.pie.append("Study", 20)
        self.pie.append("Leisure", 30)
        self.pie.append("Sleep", 40)

        self.pie.setLabelsVisible(True)
        self.pie.setHoleSize(0.5)

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.pie)
        self.chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.chart.setBackgroundRoundness(10)

        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        ########################################

        self.bar = QtCharts.QBarSet("Minutes")

        categories = ["Work", "Study", "Leisure", "Sleep"]
        minutes = [10, 20, 30, 40]
        for minute in minutes:
            self.bar.append(minute)

        self.bar_series = QtCharts.QHorizontalBarSeries()
        self.bar_series.setLabelsVisible(True)
        self.bar_series.setLabelsFormat("@value min(s)")

        self.bar_series.setLabelsPosition(QtCharts.QAbstractBarSeries.LabelsPosition.LabelsOutsideEnd)
        self.bar_series.append(self.bar)

        self.bar_chart = QtCharts.QChart()
        self.bar_chart.addSeries(self.bar_series)
        self.bar_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.bar_chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.bar_chart.setBackgroundRoundness(10)
        self.bar_chart.legend().hide()

        self.axis_x = QtCharts.QValueAxis()
        self.axis_x.setLabelFormat("%i")
        self.axis_x.setTitleText("Minutes")
        self.axis_x.setGridLineVisible(False)
        self.bar_chart.setAxisX(self.axis_x, self.bar_series)

        self.axis_y = QtCharts.QBarCategoryAxis()
        self.axis_y.append(categories)
        self.axis_y.setGridLineVisible(False)
        self.bar_chart.setAxisY(self.axis_y, self.bar_series)

        self.bar_chart_view = QtCharts.QChartView(self.bar_chart)
        self.bar_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        ############################################

        self.button3 = QPushButton("Button 3")
        self.button4 = QPushButton("Button 4")

        self.chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.bar_chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.chart_view.setMinimumSize(300, 300)
        self.bar_chart_view.setMinimumSize(300, 300)
        self.button3.setMinimumSize(300, 300)
        self.button4.setMinimumSize(300, 300)

        self.grid = QGridLayout()
        self.grid.addWidget(self.chart_view, 0, 0)
        self.grid.addWidget(self.bar_chart_view, 0, 1)
        self.grid.addWidget(self.button3, 1, 0)
        self.grid.addWidget(self.button4, 1, 1)

        central_widget = QWidget()
        central_widget.setLayout(self.grid)

        scroll_area = QScrollArea()
        scroll_area.setWidget(central_widget)
        scroll_area.setWidgetResizable(True)

        ###############################################################################################

        self.button5 = QPushButton("Button 1")
        self.button5.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button5.setMinimumSize(300, 300)

        self.grid2 = QGridLayout()
        self.grid2.addWidget(self.button5, 0, 0)

        central_widget2 = QWidget()
        central_widget2.setLayout(self.grid2)

        scroll_area2 = QScrollArea()
        scroll_area2.setWidget(central_widget2)
        scroll_area2.setWidgetResizable(True)

        ###############################################################################################

        tab_widget = QTabWidget()
        # set tab height
        tab_widget.setStyleSheet("""
        QTabBar::tab { 
            height: 50px; 
            width: 120px; 
            border: 0; 
            font-family: Century Gothic;
            font-size: 15px;
            font-weight: bold;
        }
        QTabBar::tab:selected { 
            border-bottom: 2px solid red; 
            color: red;
        }
        QTabWidget::pane {
            border: 0;
        }
        QTabWidget::tab-bar {
            left: 10px;
        }
        
        """)

        tab_widget.addTab(QWidget(), QIcon("assets/ReConnect Logo.png"), "")
        tab_widget.setTabEnabled(0, False)
        tab_widget.setIconSize(PySide6.QtCore.QSize(40, 40))
        tab_widget.addTab(scroll_area, "Screen Time")
        tab_widget.addTab(scroll_area2, "Focus")
        tab_widget.setCurrentIndex(1)
        # todo: set tab 0 only to width 50px

        self.setCentralWidget(tab_widget)
