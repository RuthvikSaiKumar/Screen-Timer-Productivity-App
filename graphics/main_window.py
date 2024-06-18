import dataclasses
import random

import PySide6.QtCore
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMainWindow, QGridLayout, QWidget, QScrollArea, QTabWidget, QLabel, QVBoxLayout, \
    QHBoxLayout, QPushButton, QMessageBox

from graphics.charts import PieChart, HorizontalBarChart, WeeklyVerticalBarChart


@dataclasses.dataclass
class WeekData:
    sunday: PySide6.QtCore.QDate = None
    saturday: PySide6.QtCore.QDate = None

    def set(self, sunday):
        if sunday.dayOfWeek() != 7:
            raise ValueError(f"The date provided is not a Sunday. Provided Date: {sunday.toString()}")
        self.sunday = sunday
        self.saturday = sunday.addDays(6)

    def __repr__(self):
        return f"{self.sunday.toString('dd MMM')} - {self.saturday.toString('dd MMM')}"


@dataclasses.dataclass
class AppData:
    name: str
    time: float

    def __repr__(self):
        return f"{self.name} : {self.time}"


class MainWindow(QMainWindow):
    week_selected: WeekData
    hlayout: QHBoxLayout
    pie_label: QLabel
    pie_chart: PieChart
    daily_bar_label: QLabel
    daily_bar: HorizontalBarChart
    weekly_bar_label: QLabel
    weekly_bar: WeeklyVerticalBarChart
    previous_week_button: QPushButton
    next_week_button: QPushButton
    week_layout: QHBoxLayout
    app_scroll_list: QScrollArea
    app_usage_list_label: QLabel

    def __init__(self):
        super().__init__()

        self.init_window()

        ###############################################################################################

        # todo: add a button to switch between dark and light theme
        # todo: add a ? button at bottom right corner to show help : Getting Started

        self.create_title_bar()

        self.test_app_data = [AppData(f"App{i}", random.randrange(1, 10) / 2) for i in range(1, 6)]

        self.create_pie_chart()
        self.create_daily_bar_chart()
        self.create_weekly_bar_chart()
        self.create_app_list()

        ############################################

        self.grid = QGridLayout()
        self.grid.addWidget(self.pie_label, 0, 0)
        self.grid.addWidget(self.daily_bar_label, 0, 1)
        self.grid.addWidget(self.weekly_bar_label, 2, 0)
        self.grid.addWidget(self.app_usage_list_label, 2, 1)
        self.grid.addWidget(self.pie_chart.chart_view, 1, 0)
        self.grid.addWidget(self.daily_bar.bar_chart_view, 1, 1)
        self.grid.addLayout(self.week_layout, 3, 0, 2, 1)
        self.grid.addWidget(self.app_scroll_list, 3, 1, 2, 1)

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

    def init_window(self):
        self.setWindowTitle("ReConnect - Productivity Tracker")
        self.setGeometry(200, 100, 600, 600)
        self.setMinimumSize(900, 600)
        icon = QIcon("assets/ReConnect Logo.png")
        self.setWindowIcon(icon)
        self.setStyleSheet("""
                background-color: #021002;
        """)
        # self.setWindowFlag(Qt.WindowType.FramelessWindowHint)

    def create_title_bar(self):
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

    def create_pie_chart(self):
        self.pie_label = QLabel("Daily App Usage")
        self.pie_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pie_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.pie_chart = PieChart()
        for app in self.test_app_data:
            self.pie_chart.add(app.name, app.time)

    def create_daily_bar_chart(self):
        self.daily_bar_label = QLabel("Daily App Usage (Top 5)")
        self.daily_bar_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.daily_bar_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        # todo: show only top 5 or 6 apps
        self.daily_bar = HorizontalBarChart()
        for app in self.test_app_data:
            self.daily_bar.add(app.name, app.time)

    def create_weekly_bar_chart(self):
        current_day_of_week = PySide6.QtCore.QDate.currentDate().dayOfWeek()
        self.week_selected = WeekData()
        self.week_selected.set(PySide6.QtCore.QDate.currentDate().addDays(-current_day_of_week))

        self.weekly_bar_label = QLabel(f"Weekly Screen Time ({self.week_selected})")
        self.weekly_bar_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.weekly_bar_label.setStyleSheet("""
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
        self.previous_week_button.clicked.connect(self.previous_week_button_clicked)

        self.next_week_button = QPushButton(">")
        self.set_next_week_button(
            self.week_selected.sunday != PySide6.QtCore.QDate.currentDate().addDays(
                -PySide6.QtCore.QDate.currentDate().dayOfWeek()))

        self.next_week_button.setMinimumWidth(20)
        self.next_week_button.setMaximumWidth(20)
        self.next_week_button.setMinimumHeight(50)
        self.next_week_button.clicked.connect(self.next_week_button_clicked)

        self.week_layout = QHBoxLayout()
        self.week_layout.addWidget(self.previous_week_button)
        self.week_layout.addWidget(self.weekly_bar.bar_chart_view)
        self.week_layout.addWidget(self.next_week_button)
        self.week_layout.setSpacing(0)

    def create_app_list(self):
        # todo: create a subwidgets to show tabs for browser
        # todo: add a button to set a time limit for the app / tab

        self.app_usage_list_label = QLabel("App Usage List")
        self.app_usage_list_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.app_usage_list_label.setStyleSheet("""
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

        self.app_scroll_list = QScrollArea()
        self.app_scroll_list.setWidget(area)
        self.app_scroll_list.setWidgetResizable(True)
        self.app_scroll_list.verticalScrollBar().setSingleStep(10)
        self.app_scroll_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    @staticmethod
    def app_limit_button_clicked():
        notification = QMessageBox()
        # todo: rephrase this text
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

    def previous_week_button_clicked(self):
        if self.week_selected.sunday == PySide6.QtCore.QDate.currentDate().addDays(
                -PySide6.QtCore.QDate.currentDate().dayOfWeek()):
            self.set_next_week_button(True)

        self.week_selected.set(self.week_selected.sunday.addDays(-7))
        self.weekly_bar_label.setText(f"Weekly Screen Time ({self.week_selected})")

    # todo: actually update the weekly bar chart

    def next_week_button_clicked(self):
        self.week_selected.set(self.week_selected.sunday.addDays(7))
        self.weekly_bar_label.setText(f"Weekly Screen Time ({self.week_selected})")

        if self.week_selected.sunday == PySide6.QtCore.QDate.currentDate().addDays(
                -PySide6.QtCore.QDate.currentDate().dayOfWeek()):
            self.set_next_week_button(False)

    # todo: actually update the weekly bar chart

    def set_next_week_button(self, enabled: bool):
        self.next_week_button.setEnabled(enabled)
        self.next_week_button.setStyleSheet(f"""
            background-color: {"#16DB65" if enabled else "#0C7034"};
            color: #021002;
            font-family: Century Gothic;
            font-size: 16px;
            border-radius: 10px;    
            font-weight: bold;
        """)
