import random
from pprint import pprint

import PySide6.QtCharts as QtCharts
import PySide6.QtCore
from PySide6.QtGui import QPainter, QIcon, QCursor
from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget, QSizePolicy, QScrollArea, QTabWidget, \
    QToolTip


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
        # todo: remove the title bar and create custom action buttons (minimize, maximize, close)
        # todo: add a button to switch between dark and light theme
        # todo: add a left right arrow to switch between different weeks in the weekly bar chart
        # todo: sort the weekly stack chart by value in descending order

        self.pie = QtCharts.QPieSeries()
        self.pie.append("Work", 10)
        self.pie.append("Study", 20)
        self.pie.append("Leisure", 30)
        self.pie.append("Sleep", 40)

        self.pie.setLabelsVisible(True)
        # self.pie.setHoleSize(0.5)

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.pie)
        self.chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.chart.setBackgroundRoundness(10)

        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        ########################################

        self.daily_bar = QtCharts.QBarSet("Daily")
        self.daily_bar.hovered.connect(lambda status, index: self.handle_bar_hovered(status, index, self.daily_bar))

        daily_time = {
            "App1": random.randrange(1, 10) / 2,
            "App2": random.randrange(1, 10) / 2,
            "App3": random.randrange(1, 10) / 2,
            "App4": random.randrange(1, 10) / 2
        }

        daily_time = dict(sorted(daily_time.items(), key=lambda item: item[1], reverse=False))

        for time in daily_time.values():
            self.daily_bar.append(time)

        self.daily_bar_series = QtCharts.QHorizontalBarSeries()
        self.daily_bar_series.append(self.daily_bar)

        self.daily_bar_chart = QtCharts.QChart()
        self.daily_bar_chart.addSeries(self.daily_bar_series)
        self.daily_bar_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.daily_bar_chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.daily_bar_chart.setBackgroundRoundness(10)
        self.daily_bar_chart.legend().hide()

        self.daily_axis_x = QtCharts.QValueAxis()
        self.daily_axis_x.setLabelFormat("%i")  # Display labels as integers
        self.daily_axis_x.setTitleText("Time")
        self.daily_axis_x.setTickType(QtCharts.QValueAxis.TickType.TicksDynamic)
        self.daily_axis_x.setTickInterval(1)
        self.daily_axis_x.setMinorTickCount(1)
        self.daily_bar_chart.setAxisX(self.daily_axis_x, self.daily_bar_series)

        self.daily_axis_y = QtCharts.QBarCategoryAxis()
        self.daily_axis_y.append(list(daily_time.keys()))
        self.daily_axis_y.setGridLineVisible(False)
        self.daily_bar_chart.setAxisY(self.daily_axis_y, self.daily_bar_series)

        self.daily_bar_chart_view = QtCharts.QChartView(self.daily_bar_chart)
        self.daily_bar_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        ############################################

        self.weekly_bar = QtCharts.QBarSet("Weekly")
        self.weekly_bar.hovered.connect(lambda status, index: self.handle_bar_hovered(status, index, self.weekly_bar))

        week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weekly_hours = [1.5, 2.5, 3, 4.5, 5.5, 6.5, 6]
        for time in weekly_hours:
            self.weekly_bar.append(time)

        self.weekly_bar_series = QtCharts.QBarSeries()
        self.weekly_bar_series.append(self.weekly_bar)

        self.weekly_bar_chart = QtCharts.QChart()
        self.weekly_bar_chart.addSeries(self.weekly_bar_series)
        self.weekly_bar_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.weekly_bar_chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.weekly_bar_chart.setBackgroundRoundness(10)
        self.weekly_bar_chart.legend().hide()

        self.weekly_axis_x = QtCharts.QBarCategoryAxis()
        self.weekly_axis_x.append(week)
        self.weekly_axis_x.setGridLineVisible(False)
        self.weekly_bar_chart.setAxisX(self.weekly_axis_x, self.weekly_bar_series)

        self.weekly_axis_y = QtCharts.QValueAxis()
        self.weekly_axis_y.setLabelFormat("%i h")
        self.weekly_bar_chart.setAxisY(self.weekly_axis_y, self.weekly_bar_series)

        self.weekly_bar_chart_view = QtCharts.QChartView(self.weekly_bar_chart)
        self.weekly_bar_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        ############################################

        self.button4 = QPushButton("Button 4")

        self.chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.daily_bar_chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.weekly_bar_chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.chart_view.setMinimumSize(300, 300)
        self.daily_bar_chart_view.setMinimumSize(300, 300)
        self.weekly_bar_chart_view.setMinimumSize(400, 300)
        self.button4.setMinimumSize(300, 300)

        self.grid = QGridLayout()
        self.grid.addWidget(self.chart_view, 0, 0)
        self.grid.addWidget(self.daily_bar_chart_view, 0, 1)
        self.grid.addWidget(self.weekly_bar_chart_view, 1, 0)
        self.grid.addWidget(self.button4, 1, 1)

        central_widget = QWidget()
        central_widget.setLayout(self.grid)

        scroll_area = QScrollArea()
        scroll_area.setWidget(central_widget)
        scroll_area.setWidgetResizable(True)

        ###############################################################################################

        # self.button5 = QPushButton("Button 1")
        # self.button5.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        # self.button5.setMinimumSize(300, 300)
        # stacked bar chart

        self.stacked_bar = QtCharts.QStackedBarSeries()
        app1 = QtCharts.QBarSet("App1")
        app2 = QtCharts.QBarSet("App2")
        app3 = QtCharts.QBarSet("App3")
        app4 = QtCharts.QBarSet("App4")

        weekly_app_dict = {
            "Sun": {
                app1: random.randint(1, 10),
                app2: random.randint(1, 10),
                app3: random.randint(1, 10),
                app4: random.randint(1, 10)
            },
            "Mon": {
                app1: random.randint(1, 10),
                app2: random.randint(1, 10),
                app3: random.randint(1, 10),
                app4: random.randint(1, 10)
            },
            "Tue": {
                app1: random.randint(1, 10),
                app2: random.randint(1, 10),
                app3: random.randint(1, 10),
                app4: random.randint(1, 10)
            },
            "Wed": {
                app1: random.randint(1, 10),
                app2: random.randint(1, 10),
                app3: random.randint(1, 10),
                app4: random.randint(1, 10)
            },
            "Thu": {
                app1: random.randint(1, 10),
                app2: random.randint(1, 10),
                app3: random.randint(1, 10),
                app4: random.randint(1, 10)
            },
            "Fri": {
                app1: random.randint(1, 10),
                app2: random.randint(1, 10),
                app3: random.randint(1, 10),
                app4: random.randint(1, 10)
            },
            "Sat": {
                app1: random.randint(1, 10),
                app2: random.randint(1, 10),
                app3: random.randint(1, 10),
                app4: random.randint(1, 10)
            }
        }

        # sort the app dict by value in descending order
        # for week, app_dict in weekly_app_dict.items():
        #     weekly_app_dict[week] = dict(sorted(app_dict.items(), key=lambda item: item[1], reverse=True))

        for app_dict in weekly_app_dict.values():
            for app, time in app_dict.items():
                app.append(time)

        for app_dict in weekly_app_dict.values():
            for app, time in app_dict.items():
                self.stacked_bar.append(app)

        # self.stacked_bar.hovered.connect(lambda status, index: self.handle_bar_hovered(status, index,
        # self.stacked_bar))

        self.stacked_bar_series = QtCharts.QChart()
        self.stacked_bar_series.addSeries(self.stacked_bar)
        self.stacked_bar_series.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.stacked_bar_series.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.stacked_bar_series.setBackgroundRoundness(10)
        self.stacked_bar_series.legend().hide()

        self.stacked_axis_x = QtCharts.QBarCategoryAxis()
        self.stacked_axis_x.append(week)
        self.stacked_axis_x.setGridLineVisible(False)
        self.stacked_bar_series.setAxisX(self.stacked_axis_x, self.stacked_bar)

        self.stacked_axis_y = QtCharts.QValueAxis()
        self.stacked_axis_y.setLabelFormat("%i h")
        self.stacked_bar_series.setAxisY(self.stacked_axis_y, self.stacked_bar)

        self.stacked_bar_chart_view = QtCharts.QChartView(self.stacked_bar_series)
        self.stacked_bar_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.stacked_bar_chart_view.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.stacked_bar_chart_view.setMinimumSize(300, 300)

        self.grid2 = QGridLayout()
        # self.grid2.addWidget(self.button5, 0, 0)
        self.grid2.addWidget(self.stacked_bar_chart_view, 0, 0)

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
