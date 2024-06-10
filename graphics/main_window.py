from PySide6.QtWidgets import QMainWindow, QPushButton, QGridLayout, QWidget, QSizePolicy, QScrollArea, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ReConnect - Productivity Tracker")
        self.setGeometry(200, 100, 600, 600)
        self.setMinimumSize(650, 600)

        ###############################################################################################

        self.button1 = QPushButton("Button 1")
        self.button2 = QPushButton("Button 2")
        self.button3 = QPushButton("Button 3")
        self.button4 = QPushButton("Button 4")

        self.button1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button3.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.button4.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.button1.setMinimumSize(300, 300)
        self.button2.setMinimumSize(300, 300)
        self.button3.setMinimumSize(300, 300)
        self.button4.setMinimumSize(300, 300)

        self.grid = QGridLayout()
        self.grid.addWidget(self.button1, 0, 0)
        self.grid.addWidget(self.button2, 0, 1)
        self.grid.addWidget(self.button3, 1, 0)
        self.grid.addWidget(self.button4, 1, 1)

        central_widget = QWidget()
        central_widget.setLayout(self.grid)

        scroll_area = QScrollArea()
        scroll_area.setWidget(central_widget)
        scroll_area.setWidgetResizable(True)

        ###############################################################################################

        self.button8 = QPushButton("Button 8")

        self.button8.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.button8.setMinimumSize(300, 300)

        self.grid2 = QGridLayout()
        self.grid2.addWidget(self.button8, 0, 0)

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
        """)
        tab_widget.addTab(scroll_area, "Screen Time")
        tab_widget.addTab(scroll_area2, "Focus")

        self.setCentralWidget(tab_widget)
