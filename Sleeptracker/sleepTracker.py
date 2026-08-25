from PyQt6.QtWidgets import *; from PyQt6.QtCore import *
import json
import datetime
from pathlib import Path
from pprint import pprint
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
        self.dateLabel = QLabel(f"Today is {datetime.datetime.now().strftime("%A")}")

        self.table.setHorizontalHeaderLabels(["Day", "Hours"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setFixedWidth(150)
        self.table.setMaximumHeight(230) 
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        with open(script_dir/"sleepHours.json") as json_file:
            json_data = json.load(json_file)
        
        days = ["Mon", "Tus", "Wed", "Thu", "Fri", "Sat", "Sun"]
        date = datetime.datetime.now()
        print(date.strftime("%w"))
        for i in range(7):
            index_val = json_data["Current_week"][str(i+1)]
            self.table.setItem(i, 0, QTableWidgetItem(days[i]))
            self.table.setItem(i, 1, QTableWidgetItem(index_val))
        
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()
        
        layout3.addWidget(self.dateLabel)
        layout3.addWidget(self.addSleep_b)
        
        layout2.addWidget(self.table)
        layout2.addLayout(layout3)
        
        layout1.addLayout(layout2)
        layout1.addWidget(self.totalSeep_b)
        
        contianer = QWidget()
        contianer.setLayout(layout1)
        self.setCentralWidget(contianer)
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()