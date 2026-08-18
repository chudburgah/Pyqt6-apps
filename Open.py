from PyQt6.QtWidgets import *
from pathlib import Path
import sys
from Mp3Tagger.Mp3_Tagger import MainWindow as Mp3TaggerWindow; from ListApp.listApp import MainWindow as ListAppWindow; from Sleeptracker.sleepTracker import MainWindow as sleepTrackerWindow
script_dir = Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("List app")
        
        self.Mp3tagger_B = QPushButton("Open Mp3 Tagger")
        self.Mp3tagger_B.clicked.connect(self.Mp3tagger_open)
        self.ListApp_B = QPushButton("Open List App")
        self.ListApp_B.clicked.connect(self.ListApp_open)
        self.SleepTracker_b = QPushButton("Open Sleep Tracker")
        self.SleepTracker_b.clicked.connect(self.sleepTracker_open)
                
        self.Mp3TaggerSubwindow = None
        self.ListAppSubWindow = None
        self.SleepTrackerSubWindow = None
        
        layout1 = QVBoxLayout()
        
        layout1.addWidget(self.Mp3tagger_B)
        layout1.addWidget(self.ListApp_B)
        layout1.addWidget(self.SleepTracker_b)
        
        container = QWidget()
        container.setLayout(layout1)
        
        self.setCentralWidget(container)
    def Mp3tagger_open(self):
        if self.Mp3TaggerSubwindow is None:
            self.Mp3TaggerSubwindow = Mp3TaggerWindow()
            self.Mp3TaggerSubwindow.show()
        else:
            self.Mp3TaggerSubwindow.raise_()
    def ListApp_open(self):
        if self.ListAppSubWindow is None:
            self.ListAppSubWindow = ListAppWindow()
            self.ListAppSubWindow.show()
        else:
            self.ListAppSubWindow.raise_()
    def sleepTracker_open(self):
            if self.SleepTrackerSubWindow is None:
                self.SleepTrackerSubWindow = sleepTrackerWindow()
                self.SleepTrackerSubWindow.show()
            else:
                self.SleepTrackerSubWindow.raise_()
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()