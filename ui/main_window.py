import dataclasses

from PySide6.QtCore import QDate, QSize
from PySide6.QtGui import QIcon, Qt, QPixmap
from PySide6.QtWidgets import QMainWindow, QGridLayout, QScrollArea, QTabWidget, QVBoxLayout, QPushButton, \
    QHBoxLayout, QLabel, QMessageBox, QWidget, QDialog

from ui.charts import PieChart, HorizontalBarChart, WeeklyVerticalBarChart
from ui.data_reader import AppItem, read_data


@dataclasses.dataclass
class WeekData:
    sunday: QDate = None
    saturday: QDate = None

    def set(self, sunday):
        if sunday.dayOfWeek() != 7:
            raise ValueError(f"The date provided is not a Sunday. Provided Date: {sunday.toString()}")
        self.sunday = sunday
        self.saturday = sunday.addDays(6)

    def __repr__(self):
        return f"{self.sunday.toString('dd MMM')} - {self.saturday.toString('dd MMM')}"


class MainWindow(QMainWindow):
    date_label: QLabel
    update_button: QPushButton
    settings_button: QPushButton
    feedback_button: QPushButton
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

        self.create_title_bar()

        # DATA
        self.loaded_data = read_data()

        self.create_pie_chart()
        self.create_daily_bar_chart()
        self.create_weekly_bar_chart()
        self.create_app_list()

        # todo: create a refresh button to reload the data

        area = QWidget()
        area.setStyleSheet("""
            background-color: #38AD6B;
            border-radius: 10px;
        """)
        dummy_layout = QGridLayout()
        dummy_layout.addWidget(self.app_scroll_list, 0, 0)
        dummy_layout.setContentsMargins(5, 5, 5, 5)
        area.setLayout(dummy_layout)

        ############################################

        self.grid = QGridLayout()
        self.grid.addWidget(self.pie_label, 0, 0)
        self.grid.addWidget(self.daily_bar_label, 0, 1)
        self.grid.addWidget(self.weekly_bar_label, 2, 0)
        self.grid.addWidget(self.app_usage_list_label, 2, 1)
        self.grid.addWidget(self.pie_chart.chart_view, 1, 0)
        self.grid.addWidget(self.daily_bar.bar_chart_view, 1, 1)
        self.grid.addLayout(self.week_layout, 3, 0, 2, 1)
        self.grid.addWidget(area, 3, 1, 2, 1)

        central_widget = QWidget()
        central_widget.setLayout(self.grid)

        scroll_area = QScrollArea()
        scroll_area.setWidget(central_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.verticalScrollBar().setSingleStep(10)
        scroll_area.setStyleSheet("""
            QScrollBar { width: 10px; background-color: #021002; }
            QScrollBar::handle { background-color: #38AD6B; }
            QScrollBar::add-line, QScrollBar::sub-line { background: none; }
            QScrollBar::add-page, QScrollBar::sub-page { background: none; }
        """)

        ###############################################################################################

        self.focus_label = QLabel("Feature Coming Soon")
        self.focus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.create_feedback_button()
        self.create_settings_button()
        self.create_update_button()
        self.create_date_display()

        left_layout = QHBoxLayout()
        left_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        left_layout.addWidget(self.date_label)

        right_layout = QHBoxLayout()
        right_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(self.update_button)
        right_layout.addWidget(self.settings_button)
        right_layout.addWidget(self.feedback_button)
        right_layout.addWidget(self.switch_theme_button)
        right_layout.addWidget(self.help_button)
        right_layout.addWidget(self.github)

        bottom_bar = QHBoxLayout()
        bottom_bar.addLayout(left_layout)
        bottom_bar.addLayout(right_layout)

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
        image.setPixmap(QPixmap("assets/ReConnect Logo.png"))
        image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image.setScaledContents(True)
        image.setMinimumSize(50, 50)
        image.setMaximumSize(50, 50)

        title = QLabel("ReConnect")
        title.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        title.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 24px;
            color: #38AD6B;
            font-weight: bold;
        """)

        self.hlayout = QHBoxLayout()
        self.hlayout.addWidget(image)
        self.hlayout.addSpacing(20)
        self.hlayout.addWidget(title)

    def create_pie_chart(self):
        self.pie_label = QLabel("Daily App Usage %")
        self.pie_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pie_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.pie_chart = PieChart()

        dates = list(self.loaded_data.keys())
        for date in dates:
            if date == QDate.currentDate().toString("yyyy-MM-dd"):
                for app in self.loaded_data[date]:
                    self.pie_chart.add(app.name, app.time)

    def create_daily_bar_chart(self):
        self.daily_bar_label = QLabel("Daily App Usage (Top 5)")
        self.daily_bar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.daily_bar_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        self.daily_bar = HorizontalBarChart()

        dates = list(self.loaded_data.keys())
        app_time_sorted = next((sorted(self.loaded_data[date], key=lambda app_: app_.time, reverse=True)
                                for date in dates if date == QDate.currentDate().toString("yyyy-MM-dd")),
                               [])

        for app in app_time_sorted[:5]:
            self.daily_bar.add(app.name, app.time)

    def create_weekly_bar_chart(self):
        current_day_of_week = QDate.currentDate().dayOfWeek() % 7
        self.week_selected = WeekData()
        self.week_selected.set(QDate.currentDate().addDays(-current_day_of_week))

        self.weekly_bar_label = QLabel(f"Weekly Screen Time ({self.week_selected})")
        self.weekly_bar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
                self.weekly_bar.add(QDate.fromString(date, "yyyy-MM-dd").dayOfWeek() % 7, total_time)

        self.current_week_selected = 0

        self.previous_week_button = QPushButton("<")
        self.set_previous_week_button(True)
        self.previous_week_button.setMinimumWidth(20)
        self.previous_week_button.setMaximumWidth(20)
        self.previous_week_button.setMinimumHeight(50)
        self.previous_week_button.clicked.connect(self.previous_week_button_clicked)

        self.next_week_button = QPushButton(">")
        self.set_next_week_button(self.week_selected.sunday != QDate.currentDate().addDays(-current_day_of_week))

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
        #   todo: create a button for browser to show or hide tabs
        # todo: add a button to set a time limit for the app / tab
        # todo: move the widget a little down so it aligns with the chart

        self.app_usage_list_label = QLabel("App Usage List")
        self.app_usage_list_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.app_usage_list_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        dates = list(self.loaded_data.keys())
        app_time_sorted = next((sorted(self.loaded_data[date], key=lambda app_: app_.time, reverse=True)
                                for date in dates if date == QDate.currentDate().toString("yyyy-MM-dd")), [])

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
                    image.setPixmap(QPixmap("assets/tab_sublist.png"))
                    image.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

        dummy = QWidget()
        dummy.setLayout(layout)

        self.app_scroll_list = QScrollArea()
        self.app_scroll_list.setWidget(dummy)
        self.app_scroll_list.setWidgetResizable(True)
        self.app_scroll_list.verticalScrollBar().setSingleStep(10)
        self.app_scroll_list.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.app_scroll_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.app_scroll_list.setStyleSheet("""
            QScrollBar { width: 10px; background-color: #38AD6B; }
            QScrollBar::handle { background-color: #021002; }
            QScrollBar::add-line, QScrollBar::sub-line { background: none; }
            QScrollBar::add-page, QScrollBar::sub-page { background: none; }
        """)

    def previous_week_button_clicked(self):
        # don't change the order of the below two lines
        if self.week_selected.sunday == QDate.currentDate().addDays(-(QDate.currentDate().dayOfWeek() % 7)):
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
                self.weekly_bar.add(QDate.fromString(date, "yyyy-MM-dd").dayOfWeek() % 7, total_time)

        self.current_week_selected += 1

        if self.current_week_selected >= self.week_history_limit:
            self.set_previous_week_button(False)

    def next_week_button_clicked(self):
        # don't change the order of the below two lines
        self.week_selected.set(self.week_selected.sunday.addDays(7))
        self.weekly_bar_label.setText(f"Weekly Screen Time ({self.week_selected})")

        if self.week_selected.sunday == QDate.currentDate().addDays(-(QDate.currentDate().dayOfWeek() % 7)):
            self.set_next_week_button(False)

        self.weekly_bar.hours = [0] * 7
        self.weekly_bar.bar_series.clear()
        dates = list(self.loaded_data.keys())
        for date in dates:
            if (self.week_selected.sunday.toString("yyyy-MM-dd") <= date <=
                    self.week_selected.saturday.toString("yyyy-MM-dd")):
                total_time = sum(app.time for app in self.loaded_data[date])
                self.weekly_bar.add(QDate.fromString(date, "yyyy-MM-dd").dayOfWeek() % 7, total_time)

        self.current_week_selected -= 1

        if self.current_week_selected < self.week_history_limit:
            self.set_previous_week_button(True)

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
        self.help_button.setIconSize(QSize(20, 20))
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
        # todo: make this a popup, and more visually appealing
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
        self.switch_theme_button.setIconSize(QSize(20, 20))
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
        self.github.setIconSize(QSize(20, 20))
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

    def create_feedback_button(self):
        self.feedback_button = QPushButton()
        self.feedback_button.setIcon(QIcon("assets/feedback.png"))
        self.feedback_button.setIconSize(QSize(18, 18))
        self.feedback_button.setToolTip("Feedback")
        self.feedback_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.feedback_button.setMinimumSize(30, 30)
        self.feedback_button.setMaximumSize(30, 30)

        self.feedback_button.clicked.connect(self.on_feedback_button_clicked)

    @staticmethod
    def on_feedback_button_clicked():
        import webbrowser
        # todo: change it to organization's repository
        url = "https://github.com/RuthvikSaiKumar/Screen-Timer-Productivity-App/discussions"
        webbrowser.open(url)

    def create_settings_button(self):
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon("assets/settings.png"))
        self.settings_button.setIconSize(QSize(20, 20))
        self.settings_button.setToolTip("Settings")
        self.settings_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.settings_button.setMinimumSize(30, 30)
        self.settings_button.setMaximumSize(30, 30)

        self.settings_button.clicked.connect(self.on_settings_button_clicked)

    @staticmethod
    def on_settings_button_clicked():
        # todo: make this a popup
        notification = QMessageBox()
        notification.setWindowTitle("Settings")
        notification.setText(
            "Feature Under Development\n\n"
            "This button will allow you to change the settings of the app."
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

    def create_update_button(self):
        self.update_button = QPushButton("Check Update")
        self.update_button.setStyleSheet("""
            background-color: #16DB65;
            color: #021002;
            border-radius: 10px;
            font-family: Century Gothic;
            font-size: 16px;
            font-weight: bold;
        """)
        self.update_button.setMinimumSize(130, 30)
        self.update_button.setMaximumSize(130, 30)

        self.update_button.clicked.connect(self.on_update_button_clicked)

    @staticmethod
    def on_update_button_clicked():
        # check for new releases on GitHub, and notify the user if there is a new release
        notification = QMessageBox()
        notification.setWindowTitle("Update")
        notification.setText(
            "Feature Under Development\n\n"
            "This button will allow you to update the app."
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

    def create_date_display(self):
        # a label to display the current date in the format "dd MMM, yyyy - WWW" - eg: 01 Jan, 2022 - Sun
        self.date_label = QLabel(QDate.currentDate().toString("dd MMM, yyyy - ddd"))
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            color: #16DB65;
        """)
