import PySide6.QtCharts as QtCharts
import PySide6.QtGui
import PySide6.QtWidgets


# todo: make the pie chart to show the weekly app usage, not daily
# todo: make it much more visually appealing
class PieChart:
    def __init__(self):
        self.time = {}
        self.pie = QtCharts.QPieSeries()
        self.pie.setLabelsVisible(True)
        self.pie.hovered.connect(lambda status, slice: self.handle_pie_hovered(status, slice))
        self.pie.setPieSize(1)
        # self.pie.setHoleSize(0.5)

        self.chart = QtCharts.QChart()
        self.chart.addSeries(self.pie)
        self.chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.chart.setBackgroundRoundness(10)
        self.chart.setBackgroundBrush(PySide6.QtGui.QBrush(PySide6.QtGui.QColor("#0D2818")))
        self.chart.legend().hide()

        self.chart_view = QtCharts.QChartView(self.chart)
        self.chart_view.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)

        self.chart_view.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Policy.Expanding,
                                      PySide6.QtWidgets.QSizePolicy.Policy.Expanding)
        self.chart_view.setMinimumSize(300, 300)

    def add(self, name, value):
        self.time[name] = value
        self.time = dict(sorted(self.time.items(), key=lambda item: item[1], reverse=False))

        self.pie.clear()
        for app, time in self.time.items():
            self.pie.append(app, time)
        self.chart.update()

    @staticmethod
    def handle_pie_hovered(slice, status):
        if status:
            value = slice.percentage() * 100
            category = slice.label() if len(slice.label()) <= 15 else f"{slice.label()[:15]}..."

            PySide6.QtWidgets.QToolTip.showText(PySide6.QtGui.QCursor.pos(), f"{category} : {value:.2f}%")


class HorizontalBarChart:
    def __init__(self):

        self.time = {}

        self.bar = None
        self.bar_series = None

        self.bar_chart = QtCharts.QChart()
        self.bar_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.bar_chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.bar_chart.setBackgroundRoundness(10)
        self.bar_chart.legend().hide()
        self.bar_chart.setBackgroundBrush(PySide6.QtGui.QBrush(PySide6.QtGui.QColor("#0D2818")))

        self.axis_x = QtCharts.QValueAxis()
        self.axis_x.setLabelFormat("%i h")
        self.axis_x.setTickType(QtCharts.QValueAxis.TickType.TicksDynamic)
        self.axis_x.setTickInterval(1)
        self.axis_x.setMinorTickCount(1)
        self.bar_chart.setAxisX(self.axis_x, self.bar_series)

        self.axis_y = QtCharts.QBarCategoryAxis()
        self.axis_y.setGridLineVisible(False)
        self.bar_chart.setAxisY(self.axis_y, self.bar_series)

        self.bar_chart_view = QtCharts.QChartView(self.bar_chart)
        self.bar_chart_view.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        self.bar_chart_view.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Policy.Expanding,
                                          PySide6.QtWidgets.QSizePolicy.Policy.Expanding)
        self.bar_chart_view.setMinimumSize(300, 300)

    def add(self, name, value):

        self.time[name] = value
        self.time = dict(sorted(self.time.items(), key=lambda item: item[1], reverse=False))

        self.bar = QtCharts.QBarSet("Daily")
        self.bar.hovered.connect(lambda status, index: self.handle_bar_hovered(status, index, self.bar))
        for value in self.time.values():
            self.bar.append(value)

        self.bar_series = QtCharts.QHorizontalBarSeries()
        self.bar_series.append(self.bar)

        self.bar_chart.removeAllSeries()
        self.bar_chart.addSeries(self.bar_series)

        self.axis_x.setRange(0, max(self.time.values()))

        self.axis_y.clear()
        self.axis_y.append(list(self.time.keys()))
        self.bar_chart.update()

    def handle_bar_hovered(self, status, index, bar_set):
        if status:
            value = bar_set.at(index)
            category = self.axis_y.at(index)
            category = category if len(category) <= 15 else f"{category[:15]}..."
            hours = int(value)
            minutes = int((value - hours) * 60)

            if minutes == 0:
                PySide6.QtWidgets.QToolTip.showText(PySide6.QtGui.QCursor.pos(),
                                                    f"{category} : {hours} h")
            else:
                PySide6.QtWidgets.QToolTip.showText(PySide6.QtGui.QCursor.pos(),
                                                    f"{category} : {hours} h {minutes} m")


class WeeklyVerticalBarChart:
    def __init__(self):
        self.bar = QtCharts.QBarSet("Weekly")
        self.bar.hovered.connect(lambda status, index: self.handle_bar_hovered(status, index, self.bar))

        self.week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        self.hours = [0] * 7
        for time in self.hours:
            self.bar.append(time)

        self.bar_series = QtCharts.QBarSeries()
        self.bar_series.append(self.bar)

        self.bar_chart = QtCharts.QChart()
        self.bar_chart.addSeries(self.bar_series)
        self.bar_chart.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.bar_chart.setTheme(QtCharts.QChart.ChartTheme.ChartThemeDark)
        self.bar_chart.setBackgroundRoundness(10)
        self.bar_chart.legend().hide()
        self.bar_chart.setBackgroundBrush(PySide6.QtGui.QBrush(PySide6.QtGui.QColor("#0D2818")))

        self.axis_x = QtCharts.QBarCategoryAxis()
        self.axis_x.append(self.week)
        self.axis_x.setGridLineVisible(False)
        self.bar_chart.setAxisX(self.axis_x, self.bar_series)

        self.axis_y = QtCharts.QValueAxis()
        self.axis_y.setLabelFormat("%i h")
        self.axis_y.setTickType(QtCharts.QValueAxis.TickType.TicksDynamic)
        self.axis_y.setTickInterval(1)
        self.bar_chart.setAxisY(self.axis_y, self.bar_series)

        self.bar_chart_view = QtCharts.QChartView(self.bar_chart)
        self.bar_chart_view.setRenderHint(PySide6.QtGui.QPainter.RenderHint.Antialiasing)
        self.bar_chart_view.setSizePolicy(PySide6.QtWidgets.QSizePolicy.Policy.Expanding,
                                          PySide6.QtWidgets.QSizePolicy.Policy.Expanding)
        self.bar_chart_view.setMinimumSize(300, 300)

    def add(self, day, value):

        self.hours[day] = value

        self.bar = QtCharts.QBarSet("Weekly")
        self.bar.hovered.connect(lambda status, index: self.handle_bar_hovered(status, index, self.bar))
        for time in self.hours:
            self.bar.append(time)

        self.bar_series = QtCharts.QBarSeries()
        self.bar_series.append(self.bar)

        self.bar_chart.removeAllSeries()
        self.bar_chart.addSeries(self.bar_series)

        self.axis_y.setRange(0, max(self.hours))

        self.bar_chart.update()

    @staticmethod
    def handle_bar_hovered(status, index, bar_set):

        # todo: future improvement: when added the apps in a stack chart

        if status:
            value = bar_set.at(index)
            hours = int(value)
            minutes = int((value - hours) * 60)

            if minutes == 0:
                PySide6.QtWidgets.QToolTip.showText(PySide6.QtGui.QCursor.pos(), f"{hours} h")
            else:
                PySide6.QtWidgets.QToolTip.showText(PySide6.QtGui.QCursor.pos(), f"{hours} h {minutes} m")
