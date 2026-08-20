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
        
        self.addSleep_b = QPushButton("Add sleep")
        self.table = QTableWidget()
        self.table.setRowCount(7)
        self.table.setColumnCount(2)
        self.table.setItem(1,1, QTableWidgetItem("yo bro"))
        self.table.setMaximumWidth(219) 
 #       self.table.setColumnWidth(1, 100)
#        self.table.setColumnWidth(0, 100)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        layout1 = QVBoxLayout()
        
        layout1.addWidget(self.addSleep_b)
        layout1.addWidget(self.table)
        
        contianer = QWidget()
        contianer.setLayout(layout1)
        self.setCentralWidget(contianer)
app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
