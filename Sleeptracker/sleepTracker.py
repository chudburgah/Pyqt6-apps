from PyQt6.QtWidgets import *
import json
import datetime
from pathlib import Path
import sys
script_dir = Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sleep Tracker")
        
        self.addSleep_b = QPushButton("Press Me!")

        layout1 = QVBoxLayout()
        
        layout1.addWidget(self.addSleep_b)
        
        contianer = QWidget()
        contianer.setLayout(layout1)
        self.setCentralWidget(contianer)
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
