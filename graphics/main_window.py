import random

import PySide6.QtCharts as QtCharts
import PySide6.QtCore
from PySide6.QtGui import QPainter, QIcon, QCursor
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget, QSizePolicy, QScrollArea, QTabWidget, \
    QToolTip, QLabel

from graphics import Charts


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ReConnect - Productivity Tracker")
        self.setGeometry(200, 100, 600, 600)
        self.setMinimumSize(750, 600)
        icon = QIcon("assets/ReConnect Logo.png")
        self.setWindowIcon(icon)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        ###############################################################################################

        # todo: add labels to what chart is for what
        # todo: add a button to switch between dark and light theme

        self.pie_chart = Charts.PieChart()
        self.pie_chart.add("App1", random.randrange(1, 10) / 2)
        self.pie_chart.add("App2", random.randrange(1, 10) / 2)
        self.pie_chart.add("App3", random.randrange(1, 10) / 2)
        self.pie_chart.add("App4", random.randrange(1, 10) / 2)
        self.pie_chart.add("App5", 3.4543450)

        ########################################

        self.daily_bar = Charts.HorizontalBarChart()
        self.daily_bar.add("App1", random.randrange(1, 10) / 2)
        self.daily_bar.add("App2", random.randrange(1, 10) / 2)
        self.daily_bar.add("App3", random.randrange(1, 10) / 2)
        self.daily_bar.add("App4", random.randrange(1, 10) / 2)
        self.daily_bar.add("App5", 3.4543450)

        ############################################

        self.weekly_bar = Charts.WeeklyVerticalBarChart()
        self.weekly_bar.add("Mon", random.randrange(1, 10))
        self.weekly_bar.add("Tue", random.randrange(1, 10))
        self.weekly_bar.add("Wed", random.randrange(1, 10))
        self.weekly_bar.add("Thu", random.randrange(1, 10))
        self.weekly_bar.add("Fri", random.randrange(1, 10))
        self.weekly_bar.add("Sat", random.randrange(1, 10))
        self.weekly_bar.add("Sun", random.randrange(1, 10))

        ############################################

        self.grid = QGridLayout()
        self.grid.addWidget(self.pie_chart.chart_view, 0, 0)
        self.grid.addWidget(self.daily_bar.bar_chart_view, 0, 1)
        self.grid.addWidget(self.weekly_bar.bar_chart_view, 1, 0, 1, 2)

        central_widget = QWidget()
        central_widget.setLayout(self.grid)

        scroll_area = QScrollArea()
        scroll_area.setWidget(central_widget)
        scroll_area.setWidgetResizable(True)

        ###############################################################################################

        self.focus_label = QLabel("Feature Coming Soon")
        self.focus_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.focus_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 20px;
            color: red;
        """)

        self.grid2 = QGridLayout()
        self.grid2.addWidget(self.focus_label, 0, 0)

        central_widget2 = QWidget()
        central_widget2.setLayout(self.grid2)

        scroll_area2 = QScrollArea()
        scroll_area2.setWidget(central_widget2)
        scroll_area2.setWidgetResizable(True)

        ###############################################################################################

        tab_widget = QTabWidget()
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

    @staticmethod
    def handle_bar_hovered(status, index, bar_set):
        if status:
            value = bar_set.at(index)
            hours = int(value)
            minutes = int((value - hours) * 60)

            if minutes == 0:
                QToolTip.showText(QCursor.pos(), f"{hours} h")
            else:
                QToolTip.showText(QCursor.pos(), f"{hours} h {minutes} m")
        else:
            QToolTip.hideText()
