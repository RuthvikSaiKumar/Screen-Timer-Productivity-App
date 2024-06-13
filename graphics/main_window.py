import random

import PySide6.QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget, QScrollArea, QTabWidget, QLabel, QVBoxLayout, \
    QHBoxLayout

from graphics.charts import PieChart, HorizontalBarChart, WeeklyVerticalBarChart


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ReConnect - Productivity Tracker")
        self.setGeometry(200, 100, 600, 600)
        self.setMinimumSize(750, 600)
        icon = QIcon("assets/ReConnect Logo.png")
        self.setWindowIcon(icon)
        self.setStyleSheet("""
            background-color: #021002;
        """)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        ###############################################################################################

        # todo: add labels to what chart is for what
        # todo: add a button to switch between dark and light theme
        # todo: add a ? button at bottom right corner to show help : Getting Started

        # display an image
        # tab_widget.addTab(QWidget(), QIcon("assets/ReConnect Logo.png"), "")
        # tab_widget.setTabEnabled(0, False)
        # tab_widget.setIconSize(PySide6.QtCore.QSize(40, 40))

        image = QLabel()
        image.setPixmap(PySide6.QtGui.QPixmap("assets/ReConnect Logo.png"))
        image.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        # set image size
        image.setScaledContents(True)
        image.setMinimumSize(50, 50)
        image.setMaximumSize(50, 50)

        title = QLabel("ReConnect")
        title.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 24px;
            color: #16DB65;
            font-weight: bold;
        """)

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(image)
        self.hlayout.addWidget(title)

        ###############################################################################################

        pie_label = QLabel("Daily App Usage")
        pie_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        pie_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.pie_chart = PieChart()
        self.pie_chart.add("App1", random.randrange(1, 10) / 2)
        self.pie_chart.add("App2", random.randrange(1, 10) / 2)
        self.pie_chart.add("App3", random.randrange(1, 10) / 2)
        self.pie_chart.add("App4", random.randrange(1, 10) / 2)
        self.pie_chart.add("App5", 3.4543450)

        ########################################

        daily_bar_label = QLabel("Daily App Usage")
        daily_bar_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        daily_bar_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        # todo: show only top 5 or 6 apps
        self.daily_bar = HorizontalBarChart()
        self.daily_bar.add("App1", random.randrange(1, 10) / 2)
        self.daily_bar.add("App2", random.randrange(1, 10) / 2)
        self.daily_bar.add("App3", random.randrange(1, 10) / 2)
        self.daily_bar.add("App4", random.randrange(1, 10) / 2)
        self.daily_bar.add("App5", 3.4543450)

        ############################################

        weekly_bar_label = QLabel("Weekly Screen Time")
        weekly_bar_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        weekly_bar_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.weekly_bar = WeeklyVerticalBarChart()
        self.weekly_bar.add("Mon", random.randrange(1, 10))
        self.weekly_bar.add("Tue", random.randrange(1, 10))
        self.weekly_bar.add("Wed", random.randrange(1, 10))
        self.weekly_bar.add("Thu", random.randrange(1, 10))
        self.weekly_bar.add("Fri", random.randrange(1, 10))
        self.weekly_bar.add("Sat", random.randrange(1, 10))
        self.weekly_bar.add("Sun", random.randrange(1, 10))

        ############################################

        # todo: create a new widget to the current days screen app wise and also a sub widget for the tabs
        # todo: if the app is a browser, show the website name instead of the app name
        # todo: add a button to set a time limit for the app / tab

        ############################################

        self.grid = QGridLayout()
        self.grid.addWidget(pie_label, 0, 0)
        self.grid.addWidget(daily_bar_label, 0, 1)
        self.grid.addWidget(weekly_bar_label, 2, 0, 1, 2)
        self.grid.addWidget(self.pie_chart.chart_view, 1, 0)
        self.grid.addWidget(self.daily_bar.bar_chart_view, 1, 1)
        self.grid.addWidget(self.weekly_bar.bar_chart_view, 3, 0, 1, 2)

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
            color: #16DB65;
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
            font-size: 16px;
            font-weight: bold;
        }
        QTabBar::tab:selected { 
            border-bottom: 2px solid #16DB65; 
            color: #16DB65;
        }
        QTabWidget::pane {
            border: 0;
        }
        QTabWidget::tab-bar {
            left: 10px;
        }
        
        """)

        tab_widget.addTab(scroll_area, "Screen Time")
        tab_widget.addTab(scroll_area2, "Focus")
        tab_widget.setCurrentIndex(0)
        # todo: set tab 0 only to width 50px

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(tab_widget)

        # create a dummy widget to set the layout
        self.dummy_widget = QWidget()
        self.dummy_widget.setLayout(self.vlayout)
        self.setCentralWidget(self.dummy_widget)
