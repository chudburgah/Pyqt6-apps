from PyQt6.QtWidgets import *; from PyQt6.QtCore import *
import json
import datetime
from pathlib import Path
import sys
script_dir = Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Sleep Tracker")
        self.resize(200,300)
        
        self.addSleep_b = QPushButton("Add sleep")
        self.totalSeep_b = QPushButton("Total hours slept")
        self.table = QTableWidget(7, 2)

        self.table.setHorizontalHeaderLabels(["Day", "Hours"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setFixedWidth(150)
        self.table.setMaximumHeight(230) 
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        with open(script_dir/"sleepHours.json", "r") as f:
            son = json.loads(f)
        
        days = [
            ("Mon", "?"),
            ("Tus", "?"),
            ("Wed", "?"),
            ("Thu", "?"), 
            ("Fri", "?"),
            ("Sat", "?"),
            ("Sun", "?")
        ]
        date = datetime.datetime.now()
        print(date)
        print(son)
        
        for row_idx, row_data in enumerate(days):
            for col_idx, value in enumerate(row_data):
                # Every item must be wrapped in a QTableWidgetItem
                item = QTableWidgetItem(value)
                self.table.setItem(row_idx, col_idx, item)
        
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        
        layout2.addWidget(self.table)
        layout2.addWidget(self.addSleep_b)
        
        layout1.addLayout(layout2)
        layout1.addWidget(self.totalSeep_b)
        
        contianer = QWidget()
        contianer.setLayout(layout1)
        self.setCentralWidget(contianer)
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
