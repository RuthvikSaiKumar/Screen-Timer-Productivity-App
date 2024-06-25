import dataclasses

import PySide6.QtCore
from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QMainWindow, QGridLayout, QScrollArea, QTabWidget, QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QMessageBox, QWidget, QDialog

from ui.charts import PieChart, HorizontalBarChart, WeeklyVerticalBarChart
from ui.data_reader import AppItem, read_data


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


class MainWindow(QMainWindow):
    github: QPushButton
    switch_theme_button: QPushButton
    help_button: QPushButton
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

    current_week_selected: int
    week_history_limit = 3  # indexing starts from 0

    def __init__(self):
        super().__init__()

        self.init_window()

        ###############################################################################################

        self.create_title_bar()

        # DATA ###############################################################
        self.loaded_data = read_data()
        ######################################################################

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
            color: #38AD6B;
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

        ###############################################################################################

        self.create_help_button()
        self.create_switch_theme_button()
        self.create_github_link()

        bottom_bar = QHBoxLayout()
        bottom_bar.setAlignment(Qt.AlignmentFlag.AlignRight)
        bottom_bar.addWidget(self.switch_theme_button)
        bottom_bar.addWidget(self.help_button)
        bottom_bar.addWidget(self.github)

        self.vlayout = QVBoxLayout()
        self.vlayout.addLayout(self.hlayout)
        self.vlayout.addWidget(tab_widget)
        self.vlayout.addLayout(bottom_bar)

        self.dummy_widget = QWidget()
        self.dummy_widget.setLayout(self.vlayout)
        self.setCentralWidget(self.dummy_widget)

    def init_window(self):
        self.setWindowTitle("ReConnect - Productivity Tracker")
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
            color: #38AD6B;
            font-weight: bold;
        """)

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(image)
        self.hlayout.addWidget(title)

    def create_pie_chart(self):
        self.pie_label = QLabel("Daily App Usage %")
        self.pie_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pie_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.pie_chart = PieChart()

        dates = list(self.loaded_data.keys())
        for date in dates:
            if date == PySide6.QtCore.QDate.currentDate().toString("yyyy-MM-dd"):
                for app in self.loaded_data[date]:
                    self.pie_chart.add(app.name, app.time)

    def create_daily_bar_chart(self):
        self.daily_bar_label = QLabel("Daily App Usage (Top 5)")
        self.daily_bar_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.daily_bar_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.daily_bar = HorizontalBarChart()

        dates = list(self.loaded_data.keys())
        app_time_sorted = next((sorted(self.loaded_data[date], key=lambda app_: app_.time, reverse=True)
                                for date in dates if date == PySide6.QtCore.QDate.currentDate().toString("yyyy-MM-dd")),
                               [])

        for app in app_time_sorted[:5]:
            self.daily_bar.add(app.name, app.time)

    def create_weekly_bar_chart(self):
        current_day_of_week = PySide6.QtCore.QDate.currentDate().dayOfWeek() % 7
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

        dates = list(self.loaded_data.keys())
        for date in dates:
            if (self.week_selected.sunday.toString("yyyy-MM-dd") <= date <=
                    self.week_selected.saturday.toString("yyyy-MM-dd")):
                total_time = sum(app.time for app in self.loaded_data[date])
                self.weekly_bar.add(
                    PySide6.QtCore.QDate.fromString(date, "yyyy-MM-dd").dayOfWeek() % 7, total_time)

        self.current_week_selected = 0

        self.previous_week_button = QPushButton("<")
        self.set_previous_week_button(True)
        self.previous_week_button.setMinimumWidth(20)
        self.previous_week_button.setMaximumWidth(20)
        self.previous_week_button.setMinimumHeight(50)
        self.previous_week_button.clicked.connect(self.previous_week_button_clicked)

        self.next_week_button = QPushButton(">")
        self.set_next_week_button(
            self.week_selected.sunday != PySide6.QtCore.QDate.currentDate().addDays(-current_day_of_week))

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
        # todo: create a button for browser to show or hide tabs
        # todo: add a button to set a time limit for the app / tab
        # todo: the background should not scroll
        # todo: move the widget a little down so it aligns with the chart

        self.app_usage_list_label = QLabel("App Usage List")
        self.app_usage_list_label.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
        self.app_usage_list_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        dates = list(self.loaded_data.keys())
        app_time_sorted = next((sorted(self.loaded_data[date], key=lambda app_: app_.time, reverse=True)
                                for date in dates if date == PySide6.QtCore.QDate.currentDate().toString("yyyy-MM-dd")),
                               [])

        for app in app_time_sorted:
            item = AppItem(app)
            if app.app_type == "Browser":
                layout.addWidget(item.app)
                tab_layout = QVBoxLayout()
                tab_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

                tab_time_sorted = sorted(app.browser_tabs, key=lambda tab_: tab_.time, reverse=True)

                for tab in tab_time_sorted:
                    item = AppItem(tab)

                    image = QLabel()
                    image.setPixmap(PySide6.QtGui.QPixmap("assets/tab_sublist.png"))
                    image.setAlignment(PySide6.QtCore.Qt.AlignmentFlag.AlignCenter)
                    image.setScaledContents(True)
                    image.setMinimumSize(25, 25)
                    image.setMaximumSize(25, 25)

                    tab_h_layout = QHBoxLayout()
                    tab_h_layout.addWidget(image)
                    tab_h_layout.addWidget(item.app)
                    tab_layout.addLayout(tab_h_layout)
                layout.addLayout(tab_layout)
            else:
                layout.addWidget(item.app)

        area = QWidget()
        area.setStyleSheet("""
            background-color: #38AD6B;
            border-radius: 17px;
        """)
        area.setLayout(layout)

        self.app_scroll_list = QScrollArea()
        self.app_scroll_list.setWidget(area)
        self.app_scroll_list.setWidgetResizable(True)
        self.app_scroll_list.verticalScrollBar().setSingleStep(10)
        self.app_scroll_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def previous_week_button_clicked(self):
        # don't change the order of the below two lines
        if self.week_selected.sunday == PySide6.QtCore.QDate.currentDate().addDays(
                -(PySide6.QtCore.QDate.currentDate().dayOfWeek() % 7)):
            self.set_next_week_button(True)

        self.week_selected.set(self.week_selected.sunday.addDays(-7))
        self.weekly_bar_label.setText(f"Weekly Screen Time ({self.week_selected})")

        self.weekly_bar.hours = [0] * 7
        self.weekly_bar.bar_series.clear()
        dates = list(self.loaded_data.keys())
        for date in dates:
            if (self.week_selected.sunday.toString("yyyy-MM-dd") <= date <=
                    self.week_selected.saturday.toString("yyyy-MM-dd")):
                total_time = sum(app.time for app in self.loaded_data[date])
                self.weekly_bar.add(
                    PySide6.QtCore.QDate.fromString(date, "yyyy-MM-dd").dayOfWeek() % 7, total_time)

        self.current_week_selected += 1

        if self.current_week_selected >= self.week_history_limit:
            self.set_previous_week_button(False)

        print(self.current_week_selected)

    def next_week_button_clicked(self):
        # don't change the order of the below two lines
        self.week_selected.set(self.week_selected.sunday.addDays(7))
        self.weekly_bar_label.setText(f"Weekly Screen Time ({self.week_selected})")

        if self.week_selected.sunday == PySide6.QtCore.QDate.currentDate().addDays(
                -(PySide6.QtCore.QDate.currentDate().dayOfWeek() % 7)):
            self.set_next_week_button(False)

        self.weekly_bar.hours = [0] * 7
        self.weekly_bar.bar_series.clear()
        dates = list(self.loaded_data.keys())
        for date in dates:
            if (self.week_selected.sunday.toString("yyyy-MM-dd") <= date <=
                    self.week_selected.saturday.toString("yyyy-MM-dd")):
                total_time = sum(app.time for app in self.loaded_data[date])
                self.weekly_bar.add(
                    PySide6.QtCore.QDate.fromString(date, "yyyy-MM-dd").dayOfWeek() % 7, total_time)

        self.current_week_selected -= 1

        if self.current_week_selected < self.week_history_limit:
            self.set_previous_week_button(True)

        print(self.current_week_selected)

    def set_next_week_button(self, enabled: bool):
        self.next_week_button.setEnabled(enabled)
        self.next_week_button.setStyleSheet(f"""
            background-color: {"#38AD6B" if enabled else "#0C7034"};
            color: #021002;
            font-family: Century Gothic;
            font-size: 16px;
            border-radius: 10px;    
            font-weight: bold;
        """)

    def set_previous_week_button(self, enabled: bool):
        self.previous_week_button.setEnabled(enabled)
        self.previous_week_button.setStyleSheet(f"""
            background-color: {"#38AD6B" if enabled else "#0C7034"};
            color: #021002;
            font-family: Century Gothic;
            font-size: 16px;
            border-radius: 10px;    
            font-weight: bold;
        """)

    def create_help_button(self):
        self.help_button = QPushButton()
        self.help_button.setIcon(QIcon("assets/help.png"))
        self.help_button.setIconSize(PySide6.QtCore.QSize(20, 20))
        self.help_button.setToolTip("Help / Getting Started")
        self.help_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.help_button.setMinimumSize(30, 30)
        self.help_button.setMaximumSize(30, 30)

        self.help_button.clicked.connect(self.on_help_button_clicked)

    @staticmethod
    def on_help_button_clicked():
        help_dialog = QDialog()
        help_dialog.setWindowTitle("Help")
        help_dialog.setMinimumSize(800, 400)
        help_dialog.setStyleSheet("""
                background-color: #021002;
        """)
        help_dialog.setWindowIcon(QIcon("assets/ReConnect Logo.png"))

        with open("assets/help.txt", "r") as file:
            help_text = file.read()
        help_text = QLabel(help_text)

        help_text.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        layout = QVBoxLayout()
        layout.addWidget(help_text)
        help_dialog.setLayout(layout)

        help_dialog.exec()

    def create_switch_theme_button(self):
        self.switch_theme_button = QPushButton()
        self.switch_theme_button.setIcon(QIcon("assets/theme.png"))
        self.switch_theme_button.setIconSize(PySide6.QtCore.QSize(20, 20))
        self.switch_theme_button.setToolTip("Switch Theme")
        self.switch_theme_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.switch_theme_button.setMinimumSize(30, 30)
        self.switch_theme_button.setMaximumSize(30, 30)

        self.switch_theme_button.clicked.connect(self.on_switch_theme_button_clicked)

    @staticmethod
    def on_switch_theme_button_clicked():

        # todo: switch between dark and light theme

        notification = QMessageBox()
        notification.setWindowTitle("Switch Theme")
        notification.setText(
            "Feature Under Development\n\n"
            "This button will allow you to change the theme of the app."
        )
        notification.setStandardButtons(QMessageBox.StandardButton.Ok)
        notification.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 15px;
            color: #16DB65;
        """)
        notification.setWindowIcon(QIcon("assets/ReConnect Logo.png"))
        notification.button(QMessageBox.StandardButton.Ok).setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
        """)
        notification.exec()

    def create_github_link(self):
        self.github = QPushButton()
        self.github.setIcon(QIcon("assets/github.png"))
        self.github.setIconSize(PySide6.QtCore.QSize(20, 20))
        self.github.setToolTip("Open GitHub Repository")
        self.github.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.github.setMinimumSize(30, 30)
        self.github.setMaximumSize(30, 30)

        self.github.clicked.connect(self.on_github_clicked)

    @staticmethod
    def on_github_clicked():
        import webbrowser
        # todo: change it to organization's repository
        url = "https://github.com/RuthvikSaiKumar/Screen-Timer-Productivity-App"
        webbrowser.open(url)
