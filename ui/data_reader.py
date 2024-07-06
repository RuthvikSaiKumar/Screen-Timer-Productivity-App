import json

from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QPushButton, QMessageBox


def float_to_time(time: float):
    hours = int(time)
    minutes = int((time - hours) * 60)
    seconds = int((time - hours - minutes / 60) * 3600)

    # todo: better way to do this
    if hours != 0 and minutes == 0:
        return f"{hours} hr"
    if hours == 0 and minutes != 0:
        return f"{minutes} min"
    if hours == 0 and minutes == 0:
        return f"{seconds} sec"

    return f"{hours} hr {minutes} min"


def time_to_float(time: str):
    #     time format: "hh:mm:ss"
    time = time.split(':')
    hours = int(time[0])
    minutes = int(time[1])
    seconds = int(time[2])

    if hours < 0 or minutes < 0 or seconds < 0:
        raise ValueError("Time cannot be negative")

    return hours + minutes / 60 + seconds / 3600


class DataInterface:
    name: str
    time: float
    data_type: str

    def __init__(self, name, time):
        self.name = name
        self.time = time

    def __repr__(self):
        return f"{self.name} : {self.time}"


class TabData(DataInterface):
    data_type: str = "Tab"


class AppData(DataInterface):
    app_type: str = "App"
    browser_tabs: list[TabData] = None
    data_type = "Application"

    def set_browser(self, bool_=True):
        self.app_type = "Browser" if bool_ else "App"

    def add_tab(self, tab: TabData):
        if self.app_type != "Browser":
            raise ValueError(f"The app {self.name} is not a browser.")

        if self.browser_tabs is None:
            self.browser_tabs = []

        self.browser_tabs.append(tab)

    def __repr__(self):
        return f"{self.name} ({self.app_type}) : {self.time}"


class AppItem:
    def __init__(self, appdata: DataInterface):
        self.app = QWidget()
        self.app.setStyleSheet("""
            background-color: #021002;
            border-radius: 15px;
        """)
        self.app.setMinimumHeight(50)
        self.app.setMaximumHeight(50)

        max_length = 20
        self.app_name = QLabel(appdata.name if len(appdata.name) <= max_length else f"{appdata.name[:max_length]}...")
        self.app_name.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.app_name.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
            margin-left: 5px;
        """)
        self.app_name.setToolTip(appdata.name)

        self.app_time = QLabel(float_to_time(appdata.time))
        self.app_time.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.app_time.setStyleSheet("""
            font-family: Century Gothic;
            font-size: 16px;
        """)

        self.app_set_app_limit = QPushButton()
        self.app_set_app_limit.setStyleSheet("""
            background-color: #38AD6B;
            color: #021002;
            border-radius: 10px;
        """)
        self.app_set_app_limit.setMaximumSize(30, 30)
        self.app_set_app_limit.setMinimumSize(30, 30)
        self.app_set_app_limit.setIcon(QIcon("assets/timer.png"))
        self.app_set_app_limit.setToolTip("App time limit notifier")
        self.app_set_app_limit.clicked.connect(self.app_limit_button_clicked)

        self.app_layout = QHBoxLayout()
        self.app_layout.addWidget(self.app_name, 2)
        self.app_layout.addWidget(self.app_time, 1)
        self.app_layout.addWidget(self.app_set_app_limit, 1)

        self.app.setLayout(self.app_layout)

    @staticmethod
    def app_limit_button_clicked():
        notification = QMessageBox()
        notification.setWindowTitle("App Limit")
        notification.setText(
            "Feature Under Development\n\n"
            "This button will allow you to set a time limit for app usage. \n"
            "You will be notified once the limit is exceeded."
        )
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


# self.test_app_data = [AppData(f"App{i}", random.randrange(1, 10) / 2) for i in range(random.randrange(0, 7))]
# browser = AppData("Browser", random.randrange(1, 10) / 2)
# browser.set_browser()
# for i in range(random.randrange(0, 7)):
#     browser.add_tab(TabData(f"Tab{i}", random.randrange(1, 10) / 2))
# if browser.browser_tabs is None:
#     browser.browser_tabs = []
# self.test_app_data.append(browser)


def read_data():
    json_string = json.loads(open('assets/data/test.json').read())

    total_data = {}

    for i in range(len(json_string)):
        current = json_string[i]
        for date in current:
            # print(date)

            loaded_app_data = []

            for app in current[date]:
                # print(app, '-', current[date][app]['app_type'], ':', current[date][app]['time_spent'])

                if current[date][app]['app_type'] == 'Application':
                    loaded_app_data.append(AppData(app, time_to_float(current[date][app]['time_spent'])))

                if current[date][app]['app_type'] == 'Browser':
                    browser = AppData(app, time_to_float(current[date][app]['time_spent']))
                    browser.set_browser()
                    for tab in current[date][app]['tabs']:
                        browser.add_tab(TabData(tab, time_to_float(current[date][app]['tabs'][tab])))
                    loaded_app_data.append(browser)

                    # for tab in current[date][app]['tabs']:
                    #     print('\t', tab, ':', current[date][app]['tabs'][tab])

            total_data[date] = loaded_app_data

    return total_data
