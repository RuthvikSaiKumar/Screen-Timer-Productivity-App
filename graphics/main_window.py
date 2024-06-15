import random

import PySide6.QtCore
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget, QScrollArea, QTabWidget, QLabel, QVBoxLayout, \
    QHBoxLayout, QPushButton, QMessageBox

from graphics.charts import PieChart, HorizontalBarChart, WeeklyVerticalBarChart


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ReConnect - Productivity Tracker")
        self.setGeometry(200, 100, 600, 600)
        self.setMinimumSize(900, 600)
        icon = QIcon("assets/ReConnect Logo.png")
        self.setWindowIcon(icon)
        self.setStyleSheet("""
            background-color: #021002;
        """)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

        ###############################################################################################

        # todo: add a button to switch between dark and light theme
        # todo: add a ? button at bottom right corner to show help : Getting Started

        image = QLabel()
        image.setPixmap(PySide6.QtGui.QPixmap("assets/ReConnect Logo.png"))
        image.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
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

        daily_bar_label = QLabel("Daily App Usage (Top 5)")
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

        # todo: implement the buttons actions
        self.previous_week_button = QPushButton("<")
        self.previous_week_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            font-family: Century Gothic;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
        """)
        self.previous_week_button.setMinimumWidth(20)
        self.previous_week_button.setMaximumWidth(20)
        self.previous_week_button.setMinimumHeight(50)
        self.previous_week_button.clicked.connect(lambda: print("Previous Week"))

        self.next_week_button = QPushButton(">")
        self.next_week_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            font-family: Century Gothic;
            font-size: 16px;
            border-radius: 10px;
            font-weight: bold;
        """)
        self.next_week_button.setMinimumWidth(20)
        self.next_week_button.setMaximumWidth(20)
        self.next_week_button.setMinimumHeight(50)
        self.next_week_button.clicked.connect(lambda: print("Next Week"))

        self.week_layout = QHBoxLayout()
        self.week_layout.addWidget(self.previous_week_button)
        self.week_layout.addWidget(self.weekly_bar.bar_chart_view)
        self.week_layout.addWidget(self.next_week_button)
        self.week_layout.setSpacing(0)

        ############################################

        # todo: create a new widget to the current days screen app wise and also a sub widget for the tabs
        # todo: add a button to set a time limit for the app / tab

        app_usage_list_label = QLabel("App Usage List")
        app_usage_list_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        app_usage_list_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        # todo: somehow put this into a class

        app_list = [QWidget() for _ in range(10)]

        layout = QVBoxLayout()
        for app in app_list:
            app.setStyleSheet("""
                        background-color: #021002;
                    """)
            app.setMinimumHeight(50)

            # todo: set the text to the app name to be truncated if it is too long
            app_name = QLabel("App Name")
            app_name.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            app_name.setStyleSheet("""
                font-family: Century Gothic;
                font-size: 16px;
            """)

            app_time = QLabel("2h 30m")
            app_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
            app_time.setStyleSheet("""
                font-family: Century Gothic;
                font-size: 16px;
            """)

            app_set_app_limit = QPushButton()
            app_set_app_limit.setStyleSheet("""
                background-color: #16DB65;
                color: #021002;
                font-family: Century Gothic;
                font-size: 16px;
                border-radius: 10px;
            """)
            app_set_app_limit.setMaximumSize(30, 30)
            app_set_app_limit.setMinimumSize(30, 30)
            app_set_app_limit.setIcon(QIcon("assets/timer.png"))
            app_set_app_limit.clicked.connect(self.app_limit_button_clicked)

            app_layout = QHBoxLayout()
            app_layout.addWidget(app_name, 2)
            app_layout.addWidget(app_time, 1)
            app_layout.addWidget(app_set_app_limit, 1)

            app.setLayout(app_layout)
            layout.addWidget(app)

        area = QWidget()
        area.setStyleSheet("""
            background-color: #16DB65;
            border-radius: 10px;
        """)
        area.setLayout(layout)

        scroll_list = QScrollArea()
        scroll_list.setWidget(area)
        scroll_list.setWidgetResizable(True)
        scroll_list.verticalScrollBar().setSingleStep(10)
        scroll_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        ############################################

        self.grid = QGridLayout()
        self.grid.addWidget(pie_label, 0, 0)
        self.grid.addWidget(daily_bar_label, 0, 1)
        self.grid.addWidget(weekly_bar_label, 2, 0)
        self.grid.addWidget(app_usage_list_label, 2, 1)
        self.grid.addWidget(self.pie_chart.chart_view, 1, 0)
        self.grid.addWidget(self.daily_bar.bar_chart_view, 1, 1)
        self.grid.addLayout(self.week_layout, 3, 0, 2, 1)
        self.grid.addWidget(scroll_list, 3, 1, 2, 1)

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
            height: 40px; 
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

        self.dummy_widget = QWidget()
        self.dummy_widget.setLayout(self.vlayout)
        self.setCentralWidget(self.dummy_widget)

    @staticmethod
    def app_limit_button_clicked():
        notification = QMessageBox()
        # todo: refactor this text
        notification.setWindowTitle("App Limit")
        notification.setText(
            "Feature Coming Soon\n\n"
            "This button will set a time limit for the app and notify you when the time is crossed.")
        notification.setIcon(QMessageBox.Icon.Information)
        notification.setStandardButtons(QMessageBox.StandardButton.Ok)
        notification.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 15px;
            color: #16DB65;
        """)
        notification.setWindowIcon(QIcon("assets/ReConnect Logo.png"))
        # set border of button to be green
        notification.button(QMessageBox.StandardButton.Ok).setStyleSheet("""
            background-color: #16DB65; 
            color: #021002;
        """)
        notification.exec()
